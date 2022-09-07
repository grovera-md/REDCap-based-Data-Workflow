#!/usr/bin/env python

### Imports
from peewee import *
from matplotlib import pyplot as plt
import datetime
import math
import numpy as np
from sklearn.linear_model import LinearRegression

### Db connection
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

# Find subset of patients with at least 4 PSA date/value pairs in the last 6 months
currentDate = datetime.datetime.now()
deltaDays = 6*30
startDate = currentDate - datetime.timedelta(days=deltaDays)
queryPid = Patient.select(Patient.id, fn.Count(Psa.id).alias('count')).join(Psa).where(Psa.psa_date >= startDate).group_by(Patient).having(fn.Count(Psa.id) >= 3).limit(2).dicts()
for patient in queryPid:
    patientId = patient["id"]
    queryPsa = Psa.select(Psa.psa_date, Psa.psa_value).join(Patient).where(Patient.id == patientId).order_by(Psa.psa_date).dicts()
    data_x = []
    data_y = []

    for row in queryPsa:
        data_x.append(row["psa_date"])
        data_y.append(row["psa_value"])

    # Evaluate PSA doubling time
    timestampsList = []
    psaLogValues = []

    for dateValue in data_x:
        datetimeValue = datetime.datetime.combine(dateValue, datetime.time())
        timestamp = datetimeValue.timestamp()
        timestampsList.append(timestamp)

    for psa in data_y:
        psaLogValues.append(math.log(psa))

    x = np.array(timestampsList).reshape((-1, 1))
    y = np.array(psaLogValues)

    model = LinearRegression()
    model.fit(x, y)

    r_sq = model.score(x, y)

    dtRaw = math.log(2) / model.coef_[0]
    dtMonths = round(dtRaw / (30 * 24 * 60 * 60), 1)

    plt.plot(data_x, data_y, label='Patient id ' + str(patientId) + ' - PSAdt: ' + str(dtMonths) + ' months', marker='o')


plt.style.use("seaborn")
plt.xlabel('Time')
plt.ylabel('PSA (ng/mL)')
plt.title('PSA trend and PSAdt')
plt.legend()
plt.tight_layout()
plt.show()