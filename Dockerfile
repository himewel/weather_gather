FROM apache/airflow:2.0.1

ARG AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW_HOME $AIRFLOW_HOME

USER root
RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./start_airflow.sh $AIRFLOW_HOME/start_airflow.sh
RUN chown -R airflow $AIRFLOW_HOME/start_airflow.sh \
    && chmod +x $AIRFLOW_HOME/start_airflow.sh

USER airflow
WORKDIR $AIRFLOW_HOME

COPY ./requirements.txt $AIRFLOW_HOME/requirements.txt
RUN pip3 install --quiet --user --no-cache-dir --requirement requirements.txt

HEALTHCHECK CMD "curl --fail http://localhost:8080/ || exit 1"
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["$AIRFLOW_HOME/start_airflow.sh"]
