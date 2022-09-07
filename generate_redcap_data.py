#!/usr/bin/env python
import requests
import json
import random
import datetime
import time

# Set the REDCap API URL and Token before executing the script
redcap_api_url = 'https://redcapdemo.vanderbilt.edu/api/'
redcap_api_token = '[YOUR_REDCAP_API_TOKEN]'

# Define Record class
class Patient:
    def __init__(self, record_id):
        self.record_id = str(record_id)
        self.ssn = str(record_id)
        self.patient_complete = str(2)

class Psa:
    def __init__(self, record_id, date, value):
        self.record_id = str(record_id)
        self.redcap_repeat_instrument = 'psa'
        self.redcap_repeat_instance = None
        self.psa_date = str(date)
        self.psa_value = str(value)
        self.psa_complete = str(2)

# Generate sample data
# Change the sampleSize parameter to set the number of uploaded records
sampleSize = 1 # Thousand records
startPatientId = 1
for chunk in range(1, sampleSize+1):
    print("Generating chunk number: " + str(chunk), flush=True)
    data = []
    startId = (chunk-1)*1000 + startPatientId
    endId = chunk*1000 + startPatientId
    for patientId in range(startId, endId):
        patient = Patient(patientId)
        data.append(patient.__dict__)
        del patient

        # Generate a random number (between 1 and 10) of PSA date/value pairs for each patient
        # For the first PSA value, generate a random float between 0 and 1
        baselinePsaDate = datetime.datetime(2021, 1, 1)
        endDate = datetime.datetime.now()
        baselinePsaValue = random.random()

        for psaNum in range(random.randrange(1, 10)):
            # Generate random dates (in chronological order)
            if psaNum == 0:
                startDate = baselinePsaDate
            else:
                startDate = psaDate
            
            timeBetweenDates = endDate - startDate
            daysBetweenDates = timeBetweenDates.days
            randomNumberOfDays = random.randrange(daysBetweenDates)
            psaDate = startDate + datetime.timedelta(days=randomNumberOfDays)

            # Generate random values (with a higher probability of an overall ascending trend)
            if psaNum == 0:
                psaValue = baselinePsaValue
            else:
                # Generate a random PSA value in a range of predefined values
                lowerLimit = psaValue * 0.8
                upperLimit = psaValue * 3
                psaValue = random.uniform(lowerLimit, upperLimit)

            psa = Psa(patientId, psaDate.strftime("%Y-%m-%d"), round(psaValue, 1))
            psa.redcap_repeat_instance = psaNum + 1
            data.append(psa.__dict__)
            del psa

    # JSON Serialization
    json_data = json.dumps(data)

    # Upload JSON data to REDCap
    data = {
        'token': redcap_api_token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'overwriteBehavior': 'normal',
        'forceAutoNumber': 'true',
        'data': json_data,
        'returnContent': 'count',
        'returnFormat': 'json'
    }
    print("Uploading chunk number: " + str(chunk), flush=True)
    r = requests.post(redcap_api_url, data=data)
    print('HTTP Status: ' + str(r.status_code), flush=True)
    print(r.json(), flush=True)
    time.sleep(10)
