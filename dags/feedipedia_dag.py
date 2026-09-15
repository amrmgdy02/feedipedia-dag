from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from feedipedia_etl.config import ALL_TABLES, DAG_SCHEDULE
from feedipedia_etl.extract import (
    extract_categories,
    extract_countries,
    extract_datasheets,
    extract_family,
    extract_licenses,
    extract_parameter_classes,
    extract_parameters,
    extract_taxon,
    extract_feeds,
)

from feedipedia_etl.load import load_sqlite_tables
from feedipedia_etl.transform import transform_all

default_args = {
    "owner": "data",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="feedipedia_etl",
    description="Weekly Feedipedia API -> BigQuery & SQLite refresh",
    default_args=default_args,
    schedule_interval=DAG_SCHEDULE,
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=["feedipedia"],
    doc_md=__doc__,
) as dag:

    # 1. Define all extract tasks matching transform_all dependencies
    extract_datasheets_task = PythonOperator(
        task_id="extract_datasheets", python_callable=extract_datasheets
    )
    extract_feeds_task = PythonOperator(
        task_id="extract_feeds", python_callable=extract_feeds
    )
    extract_taxon_task = PythonOperator(
        task_id="extract_taxon", python_callable=extract_taxon
    )
    extract_family_task = PythonOperator(
        task_id="extract_family", python_callable=extract_family
    )
    extract_categories_task = PythonOperator(
        task_id="extract_categories", python_callable=extract_categories
    )
    extract_licenses_task = PythonOperator(
        task_id="extract_licenses", python_callable=extract_licenses
    )
    extract_countries_task = PythonOperator(
        task_id="extract_countries", python_callable=extract_countries
    )
    extract_parameter_classes_task = PythonOperator(
        task_id="extract_parameter_classes", python_callable=extract_parameter_classes
    )
    extract_parameters_task = PythonOperator(
        task_id="extract_parameters", python_callable=extract_parameters
    )

    # 2. Transform task
    transform_task = PythonOperator(
        task_id="transform_all", python_callable=transform_all
    )

    load_sqlite_task = PythonOperator(
        task_id="load_sqlite",
        python_callable=load_sqlite_tables,
        op_kwargs={"table_names": ALL_TABLES},
    )

    # 4. Pipeline orchestration dependencies
    extract_tasks = [
        extract_datasheets_task,
        extract_feeds_task,
        extract_taxon_task,
        extract_family_task,
        extract_categories_task,
        extract_licenses_task,
        extract_countries_task,
        extract_parameter_classes_task,
        extract_parameters_task,
    ]

    load_tasks = [
        load_sqlite_task,
    ]

    extract_tasks >> transform_task >> load_tasks