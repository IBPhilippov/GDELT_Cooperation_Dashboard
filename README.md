# GDELT_Cooperation_Dashboard
This repository contains the final project completed for the Data Engineering zoomcamp course, cohort 2024.

## Problem

This project is dedicated to the investigation of a dynamics of international cooperation in a variety of its forms. 
The dashboard created explores temporal variation of numbers and proportions of different events of international cooperation ranging from sharing intelligence or information to economic interactions. 
The dashboard allows to track the effect of the pandemics and international political crises on the general flow of interactions between countries, as well as it helps to figure out the correspondences in dynamics of different types of material cooperation.

---
## Data
The data for project is obtained from the datasets collected by [GDELT-project](https://www.gdeltproject.org). 
GDELT-project provides a collection of AI-processed reports from media which can be considered as
a database of all world events significant enough to be covered at least by some media. This project operates with [GDELT 2.0 version](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) of database and selects only events marked as material cooperation from 2019 till current day. 


## Tools

1. Docker/Docker Compose for conteinerization and easy deployment
2. Terraform for automated management of cloud infrastructure (IaC).
3. [Mage.AI](https://www.mage.ai) as an orchestrator.
4. Google Cloud Storage as data lake, Google Cloud Storage as a storage, Google BigQuery as DWH. 
5. Spark for data transformation.
6. Lookerstudio for dashboards and reporting. 


---

## How to reproduce
0. Create Google Cloud Account. Enable BigQuery API, enable Google Cloud Storage API.  
1. Install Docker + Docker-Compose on your machine. If needed, follow installation instructions for your system from Docker`s [documentation](https://docs.docker.com/engine/install/).
2. Copy files from this repository of just clone it to your working directory using git.

   ```git clone https://github.com/IBPhilippov/GDELT_Cooperation_Dashboard.git```
3. Move to appeared directory, i.e.
   ```cd gdelt_cooperation_dashboard```
4. Create a service account in Google Cloud Platform, grant it Admin/Editor access to your project, create json-key (if needed, follow the [instructions](https://cloud.google.com/iam/docs/keys-create-delete)) and upload json-file with keys to the directory gdelt_cooperation_dashboard. Alternatively, you can just copy the content of json key downloaded from GCP, and paste it into the new file created by

   ```nano credentials.json```
In any case, the json-key **must** be placed in the folder you downloaded from git. 
6. Change variables in environment.env accessing it in any convinient way. For example,
```nano environment.env```
Before you fill it
You need to insert your Google Cloud Platform project id after
```GCP_PROJECT_NAME=```
and the name of the file with json-keys after
```GOOGLE_CREDENTIALS=```

You can alter any variable here. Filled environment.env looks like this:
```
###Name of the file with credentials from service account###
GOOGLE_CREDENTIALS=credentials.json
###Id of your project###
GCP_PROJECT_NAME=myproject-id
###Location of dataset###
GCP_LOCATION=US
###Name of dataset in BigQuery###
BQ_DATASET_NAME=gdelt_cooperation
###Postfix for bucket name to enshure uniqueness###
ADDITIONAL_PART=999
###Region of your project###
DEFAULT_GCP_REGION=us-central1
```
8. Run the project with docker-compose.
   ```sudo docker compose --env-file=environment.env up```
OR
   ```sudo docker-compose --env-file=environment.env up```
depending on the way you installed docker-compose. You may also run it in detached mode, but it will we harder to track the process.
   ```sudo docker compose --env-file=environment.env up -d```
9. Wait some time. It may take from 10 minutes up to an hour depending from your machine. For example, e2-medium (25$-month instance from Google Compute Engine) will handle it in 25 minutes.
10. Check the data in your BigQuery. A table {BQ_DATASET_NAME}.events should have been appeared here and filled with the data.
11. If you need to automatically delete all tables and buckets created by the project running, run
    ```sudo docker run terraform:Dockerfile destroy -var-file varfile.tfvars -auto-approve```

---

## What it actually does and why so
0. The main concern was to create end-to-end portable product that requires minimal adjustments in settings (here presented by environment.env), and can be run without manual interventions. Therfore, after initial setup everything runs automatically.
1. When you run  ```sudo docker compose --env-file=environment.env up```, docker builds and runs two docker images: Terraform image and MageAI image. 
2. Terrafrom
   -creates a bucket on a project specified in environment.env after **GCP_PROJECT_NAME**.
The bucket is called as concatenation of GCP_PROJECT_NAME, BQ_DATASET_NAME and ADDITIONAL_PART specified in  environment.env. The bucket name is complex due to the requirements of uniqueness across GCP. If you face with error, indicating that suck bucket already exists, please change ADDITIONAL_PART (any combination of letters and numbers will work).
   -creates a datased called **BQ_DATASET_NAME** . The dataset should be non-existing before run, otherwise and error will be raised.
   -creates a table **BQ_DATASET_NAME.events** partitioned by _DateEvent_ and clustered by _Year_ and _Event_. The field _Year_ will be used below to delete and upload data, the field _Event_  will be used to group data in groups for dashboard representation.
The operations performed by Terraform are defined in /terraform/Dockerfile
4. Mage.AI creates a project called _gdelt_cooperation_ and pipeline called _gdelt_spark_. It runs the pipeline 5 times ranging the _year_ variable from 2019 to 2024.
5. During each run, the pipeline
  -recieves data from public GDELT-database in BQ using the query
``` SELECT DISTINCT GLOBALEVENTID, _PARTITIONTIME as EventTimestamp, MonthYear, Year, EventCode, Actor1CountryCode, Actor2CountryCode, Actor1Type1Code, Actor2Type1Code 
      FROM `gdelt-bq.gdeltv2.events_partitioned`
      WHERE EXTRACT(YEAR FROM (TIMESTAMP_TRUNC(_PARTITIONTIME, DAY))) = {year}
      and EventRootCode='06' ###06 is a root code for material cooperation events
      and IsRootEvent=1 ###we need only root events, not followups or discussion
      and IFNULL(Actor1CountryCode,'')!=IFNULL(Actor2CountryCode,'') ###the interactions should be international
```
   - ingests data into a bucket created by terraform
   - reads data from bucket, initiates the spark session
   - gets the dictionaries of codes from GDELT-project site using requests-module.
   - joins dictionaries with the data on events.  Using Spark, it aggregates data, counting number of unique events per each type, each actor couple, each county per day.
   - inserts aggregated data into bigquery, into table **GCP_PROJECT_NAME.BQ_DATASET_NAME.events**
The pipeline is ran from docker-compose command instruction. Preparation of Mage image to use Spark is defined in /mage/Dockerfile.
The pipeline blocks are stored in /defined in /mage_data/.
