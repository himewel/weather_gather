# INMET Weather Stations Data Gather

<p>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="Apache Airflow" src="https://img.shields.io/badge/apacheairflow-%23017cee.svg?&style=for-the-badge&logo=apache-airflow&logoColor=white"/>
<img alt="Google Cloud" src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?&style=for-the-badge&logo=google-cloud&logoColor=white"/>
<img alt="Terraform" src="https://img.shields.io/badge/terraform-%23623CE4.svg?&style=for-the-badge&logo=terraform&logoColor=white"/>
</p>

Hi, there! Here we are going to extract data from Brazil weather stations with [INMET](https://portal.inmet.gov.br/dadoshistoricos) open data files. After extraction, we structure the data (of an awful csv format) with Apache Airflow task orchestration with PythonOperator and BashOperator, then the data is uploaded to BigQuery. So, with the structured data in GCS and BigQuery, we use Apache Superset to create some charts and explore the dataset. The following diagram expands this flow.

![](./img/architecture.jpg)

How INMET gives to us the data packed in zip files organized by years (like `2000.zip` and ~), the Apache Airflow scheduler is programmed to make yearly DAG executions (just to parametrize the data extraction and manipulation, so do incremental uploads in the database). The csv headers (I said they use an awful format) are used to extract the station infos like their map coordinates (longitude, latitude and altitude). The other lines of the csv has the column titles and data (temperature, humidity, wind, dew, etc) that we still have to manipulate before read this with pandas.

So, we make data transitions between buckets like `loading_zone`, `raw`, `processed` and `dw` (in local directories). When we have readable data (at `processed` bucket), we structure then in `dim_estacoes` (data about the station locations, regions and cities) and `fact_medicoes` (metering datetime and weather data) to upload them to BigQuery (someday I need to implement a dim_dates) in a dataset called by `dw` (and shazam!).

## How to use

### Terraform

To create the resources in this project you can run the tf resources described in the `terraform` directory. To accomplish it, build the container with Terraform and gcloud installed:

```shell
# checkout to the terraform directory
cd terraform

# build the dockerfile
make build

# start the docker container with the dataset id, bucket and project names
make start \
    BQ_DATASET=<YOUR DATASET ID> \
    GCS_BUCKET=<YOUR GCS BUCKET NAME> \
    GOOGLE_CLOUD_PROJECT=<YOUR PROJECT NAME>

# login into your gcp account
make gcloud
```

So, you can enter in shell of the container and do the terraform steps like:

```shell
# to enter in the container shell
make shell

# install the project dependencies
terraform init gcp
# plan the resource application
terraform plan gcp
# create the resources as the tf files
terraform apply gcp
```

### Apache Airflow

Build up the docker container with the following command so it will get up our services, Apache Airflow (with postgres):

```shell
# checkout to the airflow directory
cd airflow

# build the docker images
make build

# start the Apache Airflow containers
make up \
    BQ_DATASET=<YOUR DATASET ID> \
    GCS_BUCKET=<YOUR GCS BUCKET NAME> \
    GOOGLE_CLOUD_PROJECT=<YOUR PROJECT NAME>
```

At this point, we suppose that you have created your GCP project with the resources in terraform. So, you can login into your GCP account and start the DAG scheduling with this:

```shell
# prompt gcloud auth login to log into your account
make gcloud

# trigger the dag in airflow
make start
```

To follow the dag run, check the Apache Airflow Webserver UI in http://localhost:8000. A DAG similar to the next image should be found in the UI:

<p align="center">
<img alt="Airflow DAG" src="./img/pipeline.png"/>
</p>

### Apache Superset

To build the charts below, enter in the Apache Superset UI at http://localhost:8088, login into your google account and import the dashboard located into `./superset/dashboards`. To plot the map charts, you need to provide an API key from [Mapbox](https://mapbox.com/)

```shell
# checkout to the superset directory
cd airflow

# build the superset docker environment
make build

# start the Apache Superset
make start \
    GOOGLE_CLOUD_PROJECT=<YOUR PROJECT NAME> \
    MAPBOX_API_KEY=<YOUR MAPBOX API KEY>

# login into your Google Cloud account
make gcloud
```

![](img/dashboard.jpg)

## References

- https://portal.inmet.gov.br/dadoshistoricos
- https://airflow.apache.org/docs/stable/howto/index.html
