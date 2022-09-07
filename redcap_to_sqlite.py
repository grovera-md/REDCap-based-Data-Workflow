#!/usr/bin/env python

# Imports
from peewee import *
import requests
import datetime
import time

# Timer API start
timerAPIStart = time.time()

# Set the REDCap API URL and Token before executing the script
redcap_api_url = 'https://redcapdemo.vanderbilt.edu/api/'
redcap_api_token = '[YOUR_REDCAP_API_TOKEN]'

# Db connection
db = SqliteDatabase("redcap.db")

class BaseModel(Model):
    class Meta:
        database = db

class Patient(BaseModel):
    redcap_patient_id = IntegerField(unique=True)
    ssn = CharField()

class Psa(BaseModel):
    patient = ForeignKeyField(Patient, backref='psa_values', on_delete='CASCADE')
    psa_date = DateField()
    psa_value = FloatField()

db.connect()

# Truncate tables
truncateQuery1 = Patient.delete()
truncateQuery1.execute()
truncateQuery2 = Psa.delete()
truncateQuery2.execute()

# REDCap API request
data = {
    'token': redcap_api_token,
    'content': 'record',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json'
}
result = requests.post(redcap_api_url, data=data)

# Timer API end
timerAPIEnd = time.time()
elapsedAPITime = timerAPIEnd - timerAPIStart
print('API Execution time:', elapsedAPITime, 'seconds')

# Timer SQLite start
timerSQLiteStart = time.time()

# JSON parsing
result_list = result.json()

patientsList = []
psaList = []

for record in result_list:
    redcap_patient_id = int(record["record_id"])

    if len(record["redcap_repeat_instrument"]) == 0:
        # The record belongs to the parent table (Patient)
        ssn = record["ssn"]

        patientsList.append({'id': redcap_patient_id, 'redcap_patient_id': redcap_patient_id, 'ssn': ssn})

    else:
        # The record belongs to one of the child tables (Psa, Pet, Treatment, Event)

        # Create a new record in the corresponding child table
        if record["redcap_repeat_instrument"] == "psa":
            psa_date = record["psa_date"]
            psa_value = record["psa_value"]
            psaList.append({'patient_id': redcap_patient_id, 'psa_date': datetime.datetime.strptime(psa_date, '%Y-%m-%d'), 'psa_value': float(psa_value)})

        else:
            print("Warning: unknown repeating instrument '" + "': the corresponding record was not saved")

with db.atomic():
    for batch in chunked(patientsList, 10000):
        Patient.insert_many(batch).execute()

    for batch in chunked(psaList, 10000):
        Psa.insert_many(batch).execute()


# Timer SQLite end
timerSQLiteEnd = time.time()

# Get the execution time
elapsedSQLiteTime = timerSQLiteEnd - timerSQLiteStart
print('SQLite Execution time:', elapsedSQLiteTime, 'seconds')
