import requests
import json
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

import datetime

import sys
import os


def _extract_covid_data():
	response = requests.get("https://api.covidtracking.com/v1/us/daily.csv")

	with open('covid_data.csv' , 'wb') as f:
		f.write(response.content)
		f.close()
def _pre_process():
	df = pd.read_csv('covid_data.csv') #load data
	df = df[df.states == 56]  #keeping only data from states 56
	df = df.drop(columns=['recovered' , 'lastModified' , 'states', 'dateChecked' , 'total' , 'posNeg' , 'hospitalized'])
	#Remove unnecessary columns
	# Rename Columns:
	df.rename(columns={
		"negative" : "pcr_test_negative",
		"positive": "pcr_test_positive"
	}, inplace= True)
	#Convert date to datetime
	df["date"] = df.date.astype('str')
	df['date'] = pd.to_datetime(df['date'] , format = '%Y%m%d')
	
	#drop nan values
	df = df.dropna()

	# Export to csv
	
	df.to_csv("clean_covid_data.csv")
		

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

def _upload_file_to_drive(file_path, drive_folder_id, service_account_key_file):
    # Set the credentials from the JSON key file
    credentials = service_account.Credentials.from_service_account_file(service_account_key_file, scopes=['https://www.googleapis.com/auth/drive'])

    # Build the Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Define the file to upload
    media = MediaFileUpload(file_path, resumable=True)

    # Create a file on Google Drive inside the specified folder
    file_metadata = {
        'name': file_path, #.split('/')[-1],  # Use the file's name as the name on Google Drive
        'parents': drive_folder_id  # ID of the destination folder on Google Drive
    }
    uploaded_file = drive_service.files().create(media_body=media, body=file_metadata).execute()

    
    print(f"File '{uploaded_file['name']}' uploaded to Google Drive with ID: {uploaded_file['id']}")

    #return uploaded_file

default_args = {
    'start_date':datetime.datetime(2023,8,30)
}

with DAG(dag_id = "load_covid_data", catchup = False, schedule_interval = "@daily", default_args=default_args) as dag:

    # Task #1 - Extract data from API
    extract_data = PythonOperator(
        task_id = "extract_data",
        python_callable=_extract_covid_data
    )

    # Task #2 - Clean data
    pre_process = PythonOperator(
        task_id = "pre_process",
        python_callable=_pre_process
    )
    

    #Task #3 - Load to drive
    upload_file_to_drive = PythonOperator(
        task_id = "upload_file_to_drive",
        python_callable=_upload_file_to_drive,
        op_kwargs={
            "file_path": "clean_covid_data.csv",  # Replacing with the path to the file
            "drive_folder_id": "1YplRI6-KVOwltCgs27ohBi6dlEr_C61F",  # Replacing with the ID of the destination folder on Google Drive
            "service_account_key_file": "id1.json"
        }
        
)

# Dependencies
    extract_data >> pre_process >> upload_file_to_drive


