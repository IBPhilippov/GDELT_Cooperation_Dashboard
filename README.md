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

