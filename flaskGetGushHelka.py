#!/usr/bin/python
# coding=utf8

from flask import Flask
from flask import request
import json
import sqlite3
import os
import re
import getGushHelka
from getGushHelka import GetGushHelka

app = Flask(__name__)

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:    # on Heroku, get a connection
    DB_NAME = "???"
    RUNNING_LOCAL = False
else:            # work locally
    DB_NAME = "dev.db"
    RUNNING_LOCAL = True
    app.debug = True # since we're local, keep debug on

def parseAddress(addr):
    rx = '[0-9\-]+'
    print addr
    building_num = re.search(rx, addr).group(0)
    street = re.sub(rx, '', addr)
    return (u'ירושלים', unicode(street.strip()), unicode(building_num.strip()))

def getGHFromDB(conn, city_name, street_name, building_num):
    rows = []
    print city_name, street_name, building_num
    for row in conn.execute('''SELECT gush, helka    
                           FROM street_gush_helka
                           WHERE city_name = ? AND street_name = ? AND building_num = ? 
                           AND gush is not null AND helka is not null''', 
                           (city_name, street_name, building_num)):
        print row
        
        rows.append({ 'gush' : row[0], 'helka': row[1] })
    return rows

def getCityStreetID(conn, city_name, street_name):
    
    for row in conn.execute('''SELECT city_id, street_id    
                           FROM street_gush_helka
                           WHERE city_name = ? AND street_name = ?''', 
                           (city_name, street_name)):
        return (row[0], row[1])
    
    return (None, None)

def setGHinDB(conn, city_id, street_id, building_num, gush, helka):
    conn.execute('''update street_gush_helka
                    set gush = ?, helka = ?
                    where city_id = ? and street_id = ? and building_num = ? ''',
                    (gush, helka, city_id, street_id, building_num))
    conn.commit()

@app.route("/getGushHelka")
def getGushHelka():
    addr = request.args.get('address', '')
    if not addr:
        return 'NONE'
    
    (city_name, street_name, building_num) = (parseAddress(addr))
    conn = sqlite3.connect(DB_NAME)
    
    rows = getGHFromDB(conn, city_name, street_name, building_num)
    if not rows:
        print "Didn't find gush and helka in database, fetching from interwebz"
        # get city id and street id
        (city_id, street_id) = getCityStreetID(conn, city_name, street_name)
        
        if city_id is None or street_id is None:
            return json.dumps('Cannot find address')        
        
        print "city_id=%s, street_id=%s" % (city_id, street_id)
        
        # fetch it from the interwebz
        gushHelka = GetGushHelka(city_id, street_id, building_num)
        print "Got it!", gushHelka
        
        # Cahce it :)
        if gushHelka:
            setGHinDB(conn, city_id, street_id, building_num, *gushHelka)
    
        # reload it from the DB 
        rows = getGHFromDB(conn, city_name, street_name, building_num)
    
    return json.dumps(rows)

if __name__ == "__main__":
    app.debug = True
    app.run()
