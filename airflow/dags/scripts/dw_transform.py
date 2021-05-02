import os
from datetime import datetime

import numpy as np
import pandas as pd
import yaml
from airflow.configuration import conf


def dw_transform(data_path, **kwargs):
    execution_date = kwargs.get("execution_date")
    full_df = pd.read_csv(f"{data_path}/processed/{execution_date.year}.csv")

    with open(f"{conf.get('core', 'dags_folder')}/dtypes.yaml", "r") as stream:
        column_types = yaml.load(stream, Loader=yaml.SafeLoader)

    full_df["data"] = full_df.data_medicao + "T" + full_df.hora
    full_df.drop(["data_medicao", "hora"], axis=1, inplace=True)
    full_df.rename(columns={"data": "data_medicao"}, inplace=True)

    full_df = normalize_columns(full_df, column_types)
    full_df = transform_dim_estacoes(full_df, data_path)

    append_medicoes(full_df, data_path)


def normalize_columns(full_df, column_types):
    for column_name in column_types["float"]:
        full_df[column_name] = full_df[column_name].astype("float")
    for column_name in column_types["string"]:
        full_df[column_name] = full_df[column_name].astype("str")
    for column_name in column_types["datetime"]:
        full_df[column_name] = pd.to_datetime(
            full_df[column_name], format="%Y-%m-%dT%H:%M:%S"
        )
    return full_df


def transform_dim_estacoes(full_df, data_path):
    columns = [
        "latitude",
        "longitude",
        "altitude",
        "regiao",
        "uf",
        "estacao",
        "codigo",
        "data_fundacao",
    ]
    column_id = "estacoes_id"

    try:
        dim_estacoes = pd.read_parquet(f"{data_path}/dw/dim_estacoes.parquet")
    except Exception:
        dim_estacoes = pd.DataFrame([], columns=columns + [column_id])

    estacoes = full_df[columns].drop_duplicates()
    estacoes.reset_index(drop=True, inplace=True)

    if not np.isnan(dim_estacoes[column_id].max()):
        index_offset = dim_estacoes[column_id].max()
    else:
        index_offset = 0

    estacoes[column_id] = estacoes.index + index_offset

    dim_estacoes = dim_estacoes.append(estacoes, ignore_index=True)
    dim_estacoes.drop_duplicates(subset=columns, keep="first", inplace=True)
    dim_estacoes.to_parquet(f"{data_path}/dw/dim_estacoes.parquet", index=False)

    full_df = full_df.merge(dim_estacoes, on=columns)
    full_df.drop(columns, axis=1, inplace=True)
    return full_df


def append_medicoes(full_df, data_path):
    columns = [
        "precipitacao_total",
        "pressao_atmosferica",
        "pressao_atmosferica_max",
        "pressao_atmosferica_min",
        "radiacao",
        "temperatura",
        "orvalho",
        "temperatura_max",
        "temperatura_min",
        "orvalho_max",
        "orvalho_min",
        "umidade_max",
        "umidade_min",
        "umidade",
        "vento_direcao",
        "vento_velocidade_max",
        "vento_velocidade",
        "data_medicao",
    ]
    column_id = "medicao_id"

    try:
        fact_medicoes = pd.read_parquet(f"{data_path}/dw/fact_medicoes.parquet")
    except Exception:
        fact_medicoes = pd.DataFrame([], columns=columns + [column_id])

    full_df.reset_index(drop=True, inplace=True)

    if fact_medicoes[column_id].max() == np.nan:
        index_offset = fact_medicoes[column_id].max()
    else:
        index_offset = 0

    full_df[column_id] = full_df.index + index_offset

    fact_medicoes = fact_medicoes.append(full_df, ignore_index=True)
    fact_medicoes.to_parquet(f"{data_path}/dw/fact_medicoes.parquet", index=False)
