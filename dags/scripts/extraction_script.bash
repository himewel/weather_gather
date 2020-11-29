#!/usr/bin/env bash

data_path=$1
base_url=$2
reference_year=$3

echo "Download datasets..."
curl -o ${data_path}/loading_zone/${reference_year}.zip \
    ${base_url}${reference_year}.zip

echo "Unpacking zip files..."
unzip -q ${data_path}/loading_zone/${reference_year}.zip -d ${data_path}/raw
