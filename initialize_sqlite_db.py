#!/usr/bin/env python

### Imports
from peewee import *

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

db.create_tables([Patient, Psa])