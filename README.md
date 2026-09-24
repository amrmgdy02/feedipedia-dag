# Feedipedia ETL

Standalone ETL pipeline that refreshes the **Feedipedia** data set, run as a
Cloud Run job (no Airflow). Data flows from the Feedipedia API into Cloud
Storage, then into BigQuery:

```
Feedipedia API ──► extract ──► transform ──► load ──► BigQuery (review dataset)
                   (parallel)   (rows in       (load job,
                                memory,        WRITE_TRUNCATE)
                                no staging)
                     │ raw NDJSON (GCS)
                     ▼
             gs://<bucket>/raw/<run_id>/
```

- **Extract** – Pulls all Feedipedia collections from the public API with
  pagination (`dags/feedipedia_etl/extract.py`, `api_client.py`) and uploads
  raw NDJSON pages to Cloud Storage. Collections run in parallel (threads).
- **Transform** – Reads the raw pages from GCS and builds the star-schema rows
  (dimensions) in memory (`transform.py`, `schemas.py`). There is **no staging
  directory** — rows go straight from transform to the loader.
- **Load** – Pushes the rows straight into the **review project's** BigQuery
  dataset with one load job per table (`NEWLINE_DELIMITED_JSON`,
  `WRITE_TRUNCATE`), auto-creating tables from `schemas.py` when missing
  (`load.py`). Promoting to production is a separate step outside this job.

All stages share one `run_id` per execution. The container exit code
(0 success / 1 failure) is the Cloud Run job result.

## Run locally

```bash
gcloud auth application-default login   # once, for local GCP access
python dags/main.py                              # one full ETL run
python dags/main.py --run-id 20240101T060000     # fixed run id
```

The Cloud Run service account (or your local ADC) needs **Storage Object
Admin** on the bucket and **BigQuery Data Editor / Job User**.

## Project layout

```
├── dags/
│   ├── main.py                  # Entrypoint: extract -> transform -> load
│   ├── feedipedia_etl/          # ETL Python package
│   │   ├── api_client.py        # Paginated API client
│   │   ├── config.py            # Endpoints, GCS/BigQuery, tables (env-driven)
│   │   ├── extract.py           # Extract functions (one per collection)
│   │   ├── transform.py         # In-memory star-schema row generation
│   │   ├── load.py              # BigQuery loader (load jobs, auto-create)
│   │   ├── schemas.py           # BigQuery schema definitions
│   │   ├── gcp_clients.py       # Shared GCS/BigQuery clients (ADC)
│   │   ├── gcp_clients.py       # Shared GCS/BigQuery clients (ADC)
│   │   └── doc_to_model.py      # Per-collection document -> row mappers
├── requirements.txt             # Container runtime deps
└── Dockerfile                   # Container image for Cloud Run
```

## Data model

Loaded tables are grouped in `dags/feedipedia_etl/config.py`:

- **Dimension tables** (9) – `dim_parameter_class`, `dim_category`,
  `dim_country`, `dim_family`, `dim_license`, `dim_parameter`, `dim_taxon`,
  `dim_datasheet`, `dim_feed`
- **Fact tables** (6) – `fct_feed_values`, `fct_datasheet_feeds`,
  `fct_datasheet_fields`, `fct_datasheet_categories`, `fct_datasheet_taxa`,
  `fct_datasheet_geo`

All 15 tables are produced on every run. Each dimension carries a surrogate `id`
and the source's natural key as `code`; fact rows reference dimensions by `id`
and are stamped with `_data_ingestion_id` (the run id) and `_ingestion_time`.

## Configuration (env vars)

| Variable | Default | Description |
|---|---|---|
| `FEEDIPEDIA_API_URL` | `https://fao-feedipedia-…/api` | Feedipedia API base |
| `FEEDIPEDIA_GCS_BUCKET` | `fao-dwh-review-feedipedia-etl` | GCS bucket for raw NDJSON pages |
| `GCP_PROJECT` | `fao-dwh-review` | BigQuery project (**review target**) |
| `BQ_DATASET` | `feedipedia` | BigQuery dataset (**review target**) |
| `BQ_LOCATION` | `europe-west1` | BigQuery location (must match the dataset) |
| `FEEDIPEDIA_get_max_workers` | `9` | Parallel extract workers |
| `FEEDIPEDIA_LOG_LEVEL` | `INFO` | Logging level |

## Deploying as a Cloud Run job

```bash
# 1. Build & push to GCP Artifact Registry
docker build -t europe-west1-docker.pkg.dev/<PROJECT>/<REPO>/feedipedia-etl:latest .
docker push europe-west1-docker.pkg.dev/<PROJECT>/<REPO>/feedipedia-etl:latest

# 2. Create the Cloud Run job
gcloud run jobs create feedipedia-etl \
    --image europe-west1-docker.pkg.dev/<PROJECT>/<REPO>/feedipedia-etl:latest \
    --region europe-west1 \
    --execute-command "python dags/main.py"
```

Grant the job's runtime service account (via `--service-account`) the Storage +
BigQuery roles listed above.
