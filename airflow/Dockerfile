FROM apache/airflow:2.1.0

ARG USER_ID
ARG GROUP_ID

ARG AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW_HOME $AIRFLOW_HOME

USER root

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
        | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
    && apt-get update -q=5 \
    && apt-get install --no-install-recommends --assume-yes -q=5 \
        unzip  \
        google-cloud-sdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./tools $AIRFLOW_HOME/tools

WORKDIR $AIRFLOW_HOME

RUN usermod -u ${USER_ID} airflow \
    && groupmod -g ${GROUP_ID} airflow \
    && chown -R airflow $AIRFLOW_HOME \
    && chmod +x $AIRFLOW_HOME/tools/*.sh

USER airflow

COPY ./requirements.txt $AIRFLOW_HOME/requirements.txt
RUN pip3 install --quiet --user --no-cache-dir --requirement requirements.txt

HEALTHCHECK CMD ["/bin/bash", "$AIRFLOW_HOME/tools/healthcheck.sh"]
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["$AIRFLOW_HOME/tools/start_airflow.sh"]
