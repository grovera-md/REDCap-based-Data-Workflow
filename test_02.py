#!/usr/bin/env python

import timeit
 
# code snippet to be executed only once
mysetup = '''
from peewee import SqliteDatabase, Model, IntegerField, CharField, ForeignKeyField, DateField, FloatField, fn
import statistics
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
'''
 
# code snippet to be measured
mycode = '''
queryPsa = Psa.select(Psa.psa_value, fn.Max(Psa.psa_date).alias('max_date')).join(Patient).group_by(Patient).dicts()
data = []
for row in queryPsa:
        data.append(row["psa_value"])
mean = statistics.mean(data)
'''
 
# timeit statement
iterations = 100
totalTime = timeit.timeit(setup=mysetup, stmt=mycode, number= iterations)
print("Single iteration execution time: " + str(totalTime/iterations))

