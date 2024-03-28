FROM apache/airflow:slim-latest
COPY ../../webscraping/* /opt/airflow/dags
COPY ./airflow_requirements /tmp
RUN python3 -m pip install -r /tmp/airflow_requirements.txt