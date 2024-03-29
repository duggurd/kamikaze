docker build -f ./airflow.dockerfile -t airflow_kamikaze .

if [ $? -eq 0 ]; then
    docker run -d -p 8080:8080 --name airflow_kamikaze airfow_kamikaze standalone
fi