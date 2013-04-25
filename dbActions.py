# -*- coding: UTF-8 -*-
import pymongo
import getStreetNames
import codecs
import re, os
from urlparse import urlparse

def getConnection():
    MONGO_URL = os.environ.get('MONGOHQ_URL')
    
    if MONGO_URL:
        conn = pymongo.Connection(MONGO_URL)
        db = conn[urlparse(MONGOHQ_URL).path[1:]]
    else:
        conn = pymongo.Connection('localhost',27017)
        db = conn['OpenTabaDB']
    return db

def writeStreetsToDB(DB):
    streets = getStreetNames.getStreetsByCity(3000)
    for (streetId,streetName) in streets:
        streetDict = dict()
        streetDict['name'] = unicode(streetName)
        streetDict['id'] = unicode(streetId)
        DB.streets.save(streetDict)

def createHouseDict(cityID,cityName,streetID,streetName,buildingNum):
    house = dict()
    house['cityID'] = cityID
    house['cityName'] = cityName
    house['streetID'] = streetID
    house['streetName'] = streetName
    house['buildingNum'] = buildingNum
    return house

def writeAllHousesToDB(DB):
    for street in DB.streets.find():
        writeStreetIDNums(street['id'],street['name'],DB)
        print "FINISHED "+street['name']

def writeStreetIDNumsToDB(streetID,streetName,DB):
    buildingNums = getStreetNames.getBuildingNumsByStreet(streetID)
    for num in buildingNums:
        house = createHouseDict('3000','ירושלים',streetID,streetName,num)
        DB.buildings.save(house)

db = getConnection()
writeStreetsToDB(db)

