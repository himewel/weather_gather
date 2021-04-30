#!/usr/bin/env bash

SCHEDULER_PID=$AIRFLOW_HOME/airflow-scheduler.pid
WEBSERVER_PID=$AIRFLOW_HOME/airflow-webserver.pid

echo "Cleaning up old PID files..."
if [ -f "$SCHEDULER_PID" ]; then
    rm -rf $SCHEDULER_PID
fi

if [ -f "$WEBSERVER_PID" ]; then
    rm -rf $WEBSERVER_PID
fi

echo "Setting up airflow metadata db..."
airflow db upgrade

echo "Creating default user..."
airflow users create \
    --role Admin \
    --username admin \
    --password admin \
    --firstname FirstName \
    --lastname LastName \
    --email name@domain.org

echo "Starting services..."
airflow scheduler -D & airflow webserver -p 8080
