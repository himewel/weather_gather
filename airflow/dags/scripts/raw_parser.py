import logging
from glob import glob
from io import StringIO

import numpy as np
import pandas as pd


def raw_parser(data_path, tmp_path, **kwargs):
    execution_date = kwargs.get("execution_date")

    logging.info(f"Listing raw files from {execution_date.year}")
    logging.info(f"Looking for file at {tmp_path}/raw/{execution_date.year}/*.CSV")
    file_list = glob(f"{tmp_path}/raw/{execution_date.year}/*.CSV")
    logging.info(f"Files found: \n{file_list}")

    if not file_list:
        raise ValueError(f"Any CSV files were found to {execution_date.year}")

    full_df = pd.DataFrame()

    for file in file_list:
        logging.info(f"Reading raw file {file}")
        raw_header, data_text = parse_csv(file)
        header = parse_header(raw_header)

        text_buffer = StringIO(data_text)
        df = pd.read_csv(text_buffer)

        for key, value in header.items():
            df[key] = value

        logging.info(f"Appending to full_df")
        full_df = full_df.append(df, ignore_index=True)

    logging.info("Mapping column names")
    full_df.rename(
        columns={
            "DATA (YYYY-MM-DD)": "data_medicao",
            "HORA (UTC)": "hora",
            "PRECIPITAÇÃO TOTAL. HORÁRIO (mm)": "precipitacao_total",
            "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO. HORARIA (mB)": "pressao_atmosferica",  # noqa
            "PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)": "pressao_atmosferica_max",  # noqa
            "PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)": "pressao_atmosferica_min",  # noqa
            "RADIACAO GLOBAL (KJ/m²)": "radiacao",
            "TEMPERATURA DO AR - BULBO SECO. HORARIA (°C)": "temperatura",
            "TEMPERATURA DO PONTO DE ORVALHO (°C)": "orvalho",
            "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)": "temperatura_max",
            "TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)": "temperatura_min",
            "TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)": "orvalho_max",
            "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)": "orvalho_min",
            "UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)": "umidade_max",
            "UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)": "umidade_min",
            "UMIDADE RELATIVA DO AR. HORARIA (%)": "umidade",
            "VENTO. DIREÇÃO HORARIA (gr) (° (gr))": "vento_direcao",
            "VENTO. RAJADA MAXIMA (m/s)": "vento_velocidade_max",
            "VENTO. VELOCIDADE HORARIA (m/s)": "vento_velocidade",
            "REGIÃO": "regiao",
            "UF": "uf",
            "ESTAÇÃO": "estacao",
            "CODIGO (WMO)": "codigo",
            "LATITUDE": "latitude",
            "LONGITUDE": "longitude",
            "ALTITUDE": "altitude",
            "DATA DE FUNDAÇÃO (YYYY-MM-DD)": "data_fundacao",
        },
        inplace=True,
    )
    logging.info(f"Data schema: \n{full_df.dtypes}")

    full_df.fillna(np.nan, inplace=True)

    output_name = f"{data_path}/processed/{execution_date.year}.csv"
    logging.info(f"Exporting file to {output_name}")
    full_df.to_csv(path_or_buf=output_name, index=False)


def parse_csv(file=""):
    raw_header = ""
    raw_text = ""

    with open(file, "rb") as stream:
        file_text = stream.read().decode("latin")
        file_parts = file_text.split("\n", 10)

        raw_header = "\n".join(file_parts[0:8])
        raw_text = "\n".join(file_parts[8:])

    header = format_header(raw_header)
    text = format_text(raw_text)
    return header, text


def format_header(header=""):
    header = header.replace(":", "=")
    header = header.replace(";", "")
    header = header.replace(",", ".")
    return header


def format_text(text=""):
    text = text.replace(",", ".")
    text = text.replace(";", ",")
    text = text.replace("-9999", "")
    text = text.replace(",\n", "\n")
    return text


def parse_header(text_header=""):
    header = {}
    for line in text_header.split("\n"):
        key, value = line.split("=")
        header[key] = value
    return header
