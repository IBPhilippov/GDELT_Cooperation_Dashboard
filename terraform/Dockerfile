FROM hashicorp/terraform:latest

ARG GCP_PROJECT_NAME
ARG DEFAULT_GCP_REGION
ARG GCP_LOCATION
ARG BQ_DATASET_NAME
ARG GCS_BUCKET_NAME
ARG GOOGLE_CREDENTIALS
ARG ADDITIONAL_PART
COPY /terraform/*.tf /app/
COPY ${GOOGLE_CREDENTIALS} /app/
COPY /terraform/*.json /app/

#ARG varlist="-var credentials=${GOOGLE_CREDENTIALS} -var project=${GCP_PROJECT_NAME} -var region=${DEFAULT_GCP_REGION} -var location=${GCP_LOCATION} -var bq_dataset_name=${BQ_DATASET_NAME}"
ARG varfile="credentials=\"${GOOGLE_CREDENTIALS}\" \nproject=\"${GCP_PROJECT_NAME}\" \nregion=\"${DEFAULT_GCP_REGION}\" \nlocation=\"${GCP_LOCATION}\" \nbq_dataset_name=\"${BQ_DATASET_NAME}\"\ngcs_bucket_name=\"${GCP_PROJECT_NAME}${BQ_DATASET_NAME}${ADDITIONAL_PART}\""
WORKDIR /app/
RUN echo -e ${varfile} > varfile.tfvars
RUN terraform init 
RUN terraform plan -var-file varfile.tfvars 
RUN terraform apply -var-file varfile.tfvars -auto-approve
