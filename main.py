# Copyright 2018 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
# flask is included with all functions 
from flask import abort #pylint: disable=E0401
from google.cloud import storage
import io,os


def drive_to_gcs(request):
    if request.method != 'GET':
        return abort(405)
    if request.args['id'] is None:
        return abort(404)
    drive_id = request.args['id']
    #Create drive client using application default credentials
    drive_service = build('drive','v3')
    #get filename from drive object https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html#get
    #pylint disabled because the object is constructed by API and not lintable
    file_name = drive_service.files().get(fileId=drive_id).execute()['name'] #pylint: disable=E1101
    print(file_name)


    # Instructions for downloading from drive from: https://developers.google.com/drive/api/v3/manage-downloads#examples
    file_request = drive_service.files().get_media(fileId=drive_id) #pylint: disable=E1101
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh,file_request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    
   

    #get bucket name from environment see: https://cloud.google.com/functions/docs/env-var#functions_env_var-python
    bucket_name = os.environ['BUCKET']
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_file(fh,rewind=True)
    return "Upload Complete"