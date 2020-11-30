# Weather Stations Data Gather

<code><img height="20" src="https://cdn.iconscout.com/icon/free/png-512/docker-226091.png"> Docker</code> +
<code><img height="20" src="https://avatars2.githubusercontent.com/u/33643075?s=280&v=4"> Airflow</code> +
<code><img height="20" src="https://www.clipartmax.com/png/middle/200-2001825_bigquery-analytics-data-warehouse-google-cloud-big-query-icon.png"> BigQuery</code> +
<code><img height="20" src="https://iconape.com/wp-content/files/yn/80805/svg/metabase.svg"> Metabase</code>

Hi, there! Here we extract data from Brazil weather stations from [INMET](https://portal.inmet.gov.br/dadoshistoricos) open database. After this we structure the data (of an awful csv format) with Airflow task orchestration with PythonOperator and BashOperator, the data is uploaded to BigQuery. Now with our structured data in the cloud, we use Metabase to create thats beautiful charts.

How INMET gives to us the data packed in zip files organized by years (like 2000.zip and 2001.zip), the Airflow scheduler is programmed to make yearly DAG executions (just to parametrize the data extraction and manipulation, so do incremental uploads in the database). The csv headers (I said they use an awful format) are used to extract the station infos like their map coordinates (longitude, latitude and altitude). The other lines of the csv has the column titles and data (temperature, humidity, wind, dew, etc) that we still have to manipulate before read this with pandas.

So, we make data transictions in buckets like `loading_zone`, `raw`, `processed` and `dw` (in local directories). When we have readable data (at `processed` bucket), we structure then in dim_estacoes (data about the station location, region and city) and fact_medicoes (metering date and time and weather data) to upload then to BigQuery (someday I need to implement a dim_dates) in a dataset called by `dw` (shazam!). The GCP service account should be named as `credentials.json` and located at `dags/credentials/credentials.json` to do this.

## How to use

Build up the docker container with the following command so it will get up our services: Airflow (with postgres) and Metaflow:

```bash
docker-compose up -d
```

If the tasks run returns a permission, the following chmod should solve this:

```bash
chmod 777 -r dags/data
```

At this point, we suppose that you have created your GCP project with a dataset named as `dw` and extracted the service account in `dags/credentials/credentials.json`. So, start the DAG scheduling with this:

```bash
docker exec airflow airflow unpause weather_data_pipeline
```

To follow the dag run, check the Airflow webserver GUI in http://localhost:8000. To build the charts below, enter in the Metabse GUI, gice the service account access and create the questions with sql files in `sql`.

![](img/map_chart.png)

![](img/line_chart.png)

![](img/dashboard.png)
