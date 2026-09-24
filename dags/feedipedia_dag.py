"""### Feedipedia ETL

Rebuilds the Feedipedia star schema in BigQuery from the Feedipedia API.

```
extract_<collection> x 9  ──►  transform_and_load
   (API ──► GCS)                (GCS ──► rows ──► BigQuery)
```

Each collection extracts in its own task, so one flaky endpoint retries alone.
Raw pages are staged as NDJSON per run; transform and load then share a single
process, because the full row set (~63k rows) is far too large for XCom. Only
the GCS prefix strings travel between tasks.

All 15 tables (9 `dim_*`, 6 `fct_*`) are rebuilt every run with WRITE_TRUNCATE.
The loader refuses to truncate any table to zero rows, so an upstream outage
fails the run instead of emptying the warehouse.

`run_id` is the run's `ts_nodash`, so a retry reuses the same GCS prefix and
extract clears it before re-staging — no double-counted pages.

**Maintainer**: Amr Magdy (amrmagdy722@gmail.com)
"""

import json
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

#######################################################
# Set the environment to use:
#   prod    for production
#   review  for development
#######################################################

ENV = "review"

#############################

AIRFLOW_DAGS = os.environ["DAGS_FOLDER"]
CONFIGFILE = f"{AIRFLOW_DAGS}/feedipedia_etl/env_config.json"
with open(CONFIGFILE, "r") as jf:
    conf_data = json.load(jf)

config = conf_data[ENV]

os.environ["GCP_PROJECT"] = config["gcp_project"]
os.environ["BQ_DATASET"] = config["bq_dataset"]
os.environ["BQ_LOCATION"] = config["bq_location"]
os.environ["FEEDIPEDIA_GCS_BUCKET"] = config["bucket"]
os.environ["FEEDIPEDIA_API_URL"] = config["api_url"]

from feedipedia_etl.extract import EXTRACT_RESOURCES
from feedipedia_etl import gcp_clients
from feedipedia_etl.load import load_bigquery_tables
from feedipedia_etl.transform import transform_all  



def _use_connection_credentials(
    gcp_conn_id: str, gcp_project: str, impersonation_sa: str | None = None
) -> None:
    """Point the ETL's GCP clients at the identity behind ``gcp_conn_id``.

    The connection defines who the pipeline runs as: with no keyfile it falls back
    to the worker's ADC, and its impersonation chain (if set) mints credentials for
    the ETL service account instead. ``impersonation_sa`` is only an override for
    the rare case of reusing a shared connection under a different identity; it is
    normally unset, and the connection is the single source of truth.

    The import is local because DAG files are re-parsed constantly by the
    scheduler, and neither the provider import nor the credential fetch belongs at
    parse time.
    """
    from airflow.providers.google.common.hooks.base_google import GoogleBaseHook

    kwargs = {"impersonation_chain": impersonation_sa} if impersonation_sa else {}
    hook = GoogleBaseHook(gcp_conn_id=gcp_conn_id, **kwargs)
    gcp_clients.configure(credentials=hook.get_credentials(), project=gcp_project)


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
) as dag:
    dag.doc_md = __doc__

    common_kwargs = {
        "run_id": "{{ ts_nodash }}",
        "gcp_conn_id": config["gcp_conn_id"],
        "gcp_project": config["gcp_project"],
        "impersonation_sa": config.get("impersonation_sa"),
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

    extract_tasks >> transform_and_load_task
