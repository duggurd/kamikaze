FROM apache/airflow:slim-latest
COPY webscraping/* /opt/airflow/dags
COPY docker/airflow/requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install -r /tmp/requirements.txt