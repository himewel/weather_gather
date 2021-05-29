FROM apache/superset

ENV SUPERSET_HOME /opt/superset
ENV PYTHONPATH ${SUPERSET_HOME}
ENV SUPERSET_CONFIG_PATH ${SUPERSET_HOME}/config/superset_config.py

USER root

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
        | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
    && apt-get update -q=5 \
    && apt-get install google-cloud-sdk --no-install-recommends -q=5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /home/superset \
    && chown -R superset /home/superset

WORKDIR ${SUPERSET_HOME}

COPY config config

RUN chown superset ${SUPERSET_HOME}/config \
    && chmod +x ${SUPERSET_HOME}/config/*

COPY requirements.txt .

RUN pip install \
    --quiet \
    --no-cache-dir \
    --requirement requirements.txt

USER superset

HEALTHCHECK CMD curl --fail http://localhost:8088 || exit 1
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ "${SUPERSET_HOME}/config/start.sh" ]
