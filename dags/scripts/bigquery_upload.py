import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def bigquery_upload(data_path="", credentials_path="", **kwargs):
    credentials = service_account.Credentials.from_service_account_file(
        f"{credentials_path}/credentials.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"])

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id
    )

    file_list = ["dim_estacoes", "fact_medicoes"]
    for table in file_list:
        df = pd.read_parquet(f"{data_path}/dw/{table}.parquet")
        load_from_dataframe(
            client=client,
            dataset_id="dw",
            table=table,
            df=df
        )


def load_from_dataframe(client, dataset_id, table, df):
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table)
    job_config = bigquery.LoadJobConfig()

    bq_schema = []
    df_schema = get_dataframe_schema(df)
    for column in df_schema.keys():
        bq_schema.append(
            bigquery.SchemaField(column, df_schema[column])
        )

    job_config.schema = bq_schema
    job_config.write_disposition = bigquery.job.WriteDisposition.WRITE_TRUNCATE

    client.load_table_from_dataframe(
        dataframe=df,
        destination=table_ref,
        job_config=job_config
    )


def get_dataframe_schema(df):
    schema = {}
    for column in df.columns:
        if 'int' in df.dtypes[column].name:
            schema[column] = 'INTEGER'
        elif 'float' in df.dtypes[column].name:
            schema[column] = 'FLOAT'
        elif 'datetime64' in df.dtypes[column].name:
            schema[column] = 'TIMESTAMP'
        elif 'object' in df.dtypes[column].name:
            schema[column] = 'STRING'
        else:
            schema[column] = 'STRING'
    return schema
