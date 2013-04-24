#!/usr/bin/python
# -*- coding: UTF-8-*-

#IMPORTS
import sqlite3, sys
import getStreetNames

def writeDB(cursor):
    """
    Gets a cursor of a DB.
    Assumes the DB has the table that holds city, street, building num, gush, helka info

     Writes into the DB all the information off the Tax website
        of all the buildings in the country
    """
    cities = getStreetNames.getCities()
    cityCounter = 0
    for city in [c for c in cities if c[0] == '3000']:
        print "STARTING ON CITY: "+ city[1].decode('utf-8')
        streets = getStreetNames.getStreetsByCity(city[0])
        streetCounter = 0
        for street in streets:
            buildingNums = getStreetNames.getBuildingNumsByStreet(street[0])
            for num in buildingNums:
                insertTuple = (city[0],city[1].decode('utf-8'),street[0],street[1].decode('utf-8'),num.decode('utf-8'))
                cursor.execute(u'INSERT into STREET_GUSH_HELKA (CITY_ID,CITY_NAME,STREET_ID,STREET_NAME,BUILDING_NUM) VALUES (?,?,?,?,?)',insertTuple)
            streetCounter = streetCounter + 1
            if streetCounter % 50 == 0:
                print "DONE "+str(streetCounter)+" STREETS"
        print "DONE WITH CITY: " + city[1].decode('utf-8')
        cityCounter = cityCounter+1
        print "CITIES LEFT: "+str(len(cities)-cityCounter)

#CHECK TO SEE THAT DB ADDRESS GIVEN
if len(sys.argv) != 2:
    print "Usage: %s <dbname>" % sys.argv[0]
    sys.exit(1)

db_name = sys.argv[1]

conn = sqlite3.connect(db_name)
writeDB(conn)
conn.commit()
conn.close()

