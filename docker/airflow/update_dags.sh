docker cp ../../webscraping/. kamikaze_airflow:/opt/airflow/dags

if [ $? -eq 0 ]; then
    docker exec kamikaze_airflow airflow dags reserialize
fi