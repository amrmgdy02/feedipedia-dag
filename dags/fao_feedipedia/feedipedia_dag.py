import json
import logging
import os
from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.models import Variable
from airflow.operators.python import PythonOperator, ShortCircuitOperator

#######################################################
# Set the environment to use:
#   prod    for production
#   review  for development
#######################################################

ENV = "review"

#############################

AIRFLOW_DAGS = os.environ["DAGS_FOLDER"]
CONFIGFILE = f"{AIRFLOW_DAGS}/fao_feedipedia/config/config.json"
with open(CONFIGFILE, "r") as jf:
    conf_data = json.load(jf)

config = conf_data[ENV]

os.environ["GCP_PROJECT"] = config["gcp_project"]
os.environ["BQ_DATASET"] = config["bq_dataset"]
os.environ["BQ_LOCATION"] = config["bq_location"]
os.environ["FEEDIPEDIA_GCS_BUCKET"] = config["bucket"]
os.environ["FEEDIPEDIA_API_URL"] = config["api_url"]

from fao_feedipedia.utils.api_client import source_fingerprint
from fao_feedipedia.utils.extract import EXTRACT_RESOURCES

from fao_feedipedia.utils import gcp_clients
from fao_feedipedia.utils.load import load_bigquery_tables
from fao_feedipedia.utils.transform import transform_all

log = logging.getLogger(__name__)



def _use_connection_credentials(
    gcp_conn_id: str, gcp_project: str, impersonation_sa: str | None = None
) -> None:
    """Point the ETL's GCP clients at the identity behind ``gcp_conn_id``.
    """
    from airflow.providers.google.common.hooks.base_google import GoogleBaseHook

    kwargs = {"impersonation_chain": impersonation_sa} if impersonation_sa else {}
    hook = GoogleBaseHook(gcp_conn_id=gcp_conn_id, **kwargs)
    gcp_clients.configure(credentials=hook.get_credentials(), project=gcp_project)


STATE_VARIABLE = f"feedipedia_{ENV}_source_fingerprint"


def check_for_updates(**context) -> bool:
    """Skip the whole run when the source has not changed since the last load.
    """
    fingerprint = source_fingerprint(EXTRACT_RESOURCES)
    context["ti"].xcom_push(key="fingerprint", value=fingerprint)

    if context["params"].get("force_refresh"):
        log.info("force_refresh set - running regardless of source state")
        return True

    previous = Variable.get(STATE_VARIABLE, default_var=None, deserialize_json=True)
    if previous is None:
        log.info("No previous fingerprint recorded - running a full refresh")
        return True

    changed = sorted(
        resource
        for resource, current in fingerprint.items()
        if previous.get(resource) != current
    )
    if not changed:
        log.info("Source unchanged across all %d collections - skipping", len(fingerprint))
        return False

    log.info("Source changed in: %s", ", ".join(changed))
    return True


def record_state(**context) -> None:
    """Persist the fingerprint, only after the load has actually succeeded."""
    fingerprint = context["ti"].xcom_pull(
        task_ids="check_for_updates", key="fingerprint"
    )
    if not fingerprint:
        raise RuntimeError("No fingerprint from check_for_updates to record")
    Variable.set(STATE_VARIABLE, fingerprint, serialize_json=True)
    log.info("Recorded source fingerprint in Airflow Variable %s", STATE_VARIABLE)


def extract_resource(
    resource: str,
    run_id: str,
    gcp_conn_id: str,
    gcp_project: str,
    impersonation_sa: str | None = None,
) -> str:
    """Stage one collection's raw pages on GCS; returns its prefix for the transform."""
    _use_connection_credentials(gcp_conn_id, gcp_project, impersonation_sa)
    return EXTRACT_RESOURCES[resource](run_id=run_id)


def transform_and_load(
    run_id: str,
    gcp_conn_id: str,
    gcp_project: str,
    impersonation_sa: str | None = None,
    **context,
) -> dict[str, int]:
    """Read the staged pages, build the star schema and load it into BigQuery."""
    _use_connection_credentials(gcp_conn_id, gcp_project, impersonation_sa)

    ti = context["ti"]
    prefixes = {
        resource: ti.xcom_pull(task_ids=f"extract_{resource}")
        for resource in EXTRACT_RESOURCES
    }
    missing = [resource for resource, prefix in prefixes.items() if not prefix]
    if missing:
        raise RuntimeError(f"No staged prefix from extract task(s): {', '.join(missing)}")

    tables = transform_all(run_id=run_id, prefixes=prefixes)
    return load_bigquery_tables(tables)


default_args = {
    "owner": "feedipedia",
    "start_date": datetime(2026, 9, 24),
    "email": config["email_list"],
    "email_on_failure": config["emails_enabled"],
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": 300,
}

with DAG(
    dag_id="feedipedia_" + ENV,
    schedule="0 3 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["feedipedia"],
    default_args=default_args,
    params={
        "force_refresh": Param(
            default=False,
            type="boolean",
            title="Force refresh",
            description="Reload every table even when the source API reports no "
            "changes since the last successful run.",
        ),
    },
) as dag:
    dag.doc_md = __doc__

    common_kwargs = {
        "run_id": "{{ ts_nodash }}",
        "gcp_conn_id": config["gcp_conn_id"],
        "gcp_project": config["gcp_project"],
        #"impersonation_sa": config.get("impersonation_sa"),
    }

    extract_tasks = [
        PythonOperator(
            task_id=f"extract_{resource}",
            python_callable=extract_resource,
            op_kwargs={"resource": resource, **common_kwargs},
        )
        for resource in EXTRACT_RESOURCES
    ]

    transform_and_load_task = PythonOperator(
        task_id="transform_and_load",
        python_callable=transform_and_load,
        op_kwargs=dict(common_kwargs),
    )

    check_task = ShortCircuitOperator(
        task_id="check_for_updates",
        python_callable=check_for_updates,
    )

    record_state_task = PythonOperator(
        task_id="record_state",
        python_callable=record_state,
    )

    check_task >> extract_tasks >> transform_and_load_task >> record_state_task
