docker cp ./webscraping/. kamikaze_airflow:/opt/airflow/dags
docker exec kamikaze_airflow airflow dags reserialize