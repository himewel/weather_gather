FROM apache/airflow:1.10.12-python3.8
ENV AIRFLOW_HOME=/home/airflow

USER root
RUN apt-get update -qqq && apt-get install unzip -q=5

USER airflow
WORKDIR /home/airflow

COPY ./requirements.txt /home/airflow/
RUN pip3 install -r requirements.txt -q --user --no-cache-dir
