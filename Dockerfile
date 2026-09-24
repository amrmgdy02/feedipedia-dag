# Feedipedia ETL — container image for a Cloud Run job.
#
# The job runs the container to completion and the process exit code is the job
# result (0 success / 1 failure). GCP wiring comes from env vars set on the job
# definition: FEEDIPEDIA_API_URL, FEEDIPEDIA_GCS_BUCKET, GCP_PROJECT, BQ_DATASET,
# BQ_LOCATION, FEEDIPEDIA_get_max_workers, FEEDIPEDIA_LOG_LEVEL. Raw NDJSON pages
# land in Cloud Storage; transformed rows are held in memory and loaded straight
# into BigQuery. The runtime service account is picked up via Application Default
# Credentials and needs Storage Object Admin on the bucket plus BigQuery Data
# Editor and Job User.
#
# Build and deploy steps are in README.md.

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Dependencies first so the layer stays cached across code changes.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) Pipeline code.
COPY dags/ ./dags/

# Run as an unprivileged user; the job only needs outbound network and its
# service-account credentials, never write access to the filesystem.
RUN useradd --create-home --uid 1000 etl \
    && chown -R etl:etl /app
USER etl

# Args passed to the job execution are appended here, so `--run-id 20260101T060000`
# works via `gcloud run jobs execute --args`. Default run id is a fresh UTC stamp.
ENTRYPOINT ["python", "dags/main.py"]
