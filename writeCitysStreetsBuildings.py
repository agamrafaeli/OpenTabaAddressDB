# -*- coding: UTF-8-*-

#HARD CODED TO WRITE TO DB THE JERUSALEM STREETS
#DO NOT USE BEFORE UNDERSTANDING

import sqlite3
import getStreetNames
import pickle
import os, sys

if len(sys.argv) != 2:
    print "Usage: %s <dbname>" % sys.argv[0]
    sys.exit(1)

db_name = sys.argv[1]

db =sqlite3.connect(db_name)
curs = db.cursor()

def writeBuildingNum(cityID,cityName,streetID,streetName,buildingNum,cursor):
    insertTuple = (cityID,cityName,streetID,streetName.decode('utf-8'),buildingNum.decode('utf-8'))
    print "Insert Tuple"
    cursor.execute(u'INSERT into STREET_GUSH_HELKA (CITY_ID,CITY_NAME,STREET_ID,STREET_NAME,BUILDING_NUM) VALUES (?,?,?,?,?)',insertTuple)
    print "WRITTEN"



def writeStreet(cityID,cityName,streetID,streetName,buildingArr,cursor):
    for building in buildingArr:
        writeBuildingNum(cityID,cityName,streetID,streetName,building,cursor)

def writeCity(cityID,cityName,cursor):
    if os.path.exists("pickleDump.pkl"):
        f=open("pickleDump.pkl","r")
        streetsArr = pickle.load(f)
        f.close()
    else:
        streetsArr = getStreetNames.getCityStreetBuildingNumsArr(cityID)
        f=open("pickleDump.pkl","w")
        pickle.dump(streetsArr,f)
        f.close()
    for street in streetsArr:
        writeStreet(cityID,cityName,street[0],street[1],street[2],cursor)

def writeIsrael(cursor):
    citysArr = getStreetNames.getCityIDS()
    for city in citysArr:
        writeCity(city[0],city[1],cursor)

writeCity(3000,u"ירושלים",curs)

curs.close()