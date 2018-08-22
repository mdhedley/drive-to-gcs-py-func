# Drive to GCS Function
This repository provides sample code for uploading files from Google Drive to Google Cloud Storage using a Python 3.7 Google Cloud Function.

## Setup
1. Activate Google Cloud functions API for your project
2. Identify the service account functions under IAM service accounts. Should resemble \<project-id>@appspot.gserviceaccount.com
3. In Drive share the folder, or object with the service account identified in step 2.
4. Create a storage bucket
5. Update BUCKET value in env.yaml with the name of the bucket that you created in step 4.
6. Deploy to cloud functions with `gcloud beta functions deploy drive_to_gcs --runtime python37 --trigger-http --env-vars-file env.yaml`
7. Call trigger the function with `curl <trigger-endpoint>?id=<drive id>`

## Known issues
Because the file streams into memory of the cloud function and then into google cloud storage you need to ensure you have enough memory to handle the file size. You can extend the memory with the --memory option for the gcloud deploy command. You can detect this issue in the log by looking for: `Error: memory limit exceeded. Function invocation was interrupted.`