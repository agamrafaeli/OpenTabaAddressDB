#!/usr/bin/python
import sqlite3
import sys

if len(sys.argv) != 2:
    print "Usage: %s <dbanme>" % sys.argv[0]
    sys.exit(1)

db_name = sys.argv[1]

# Create connection, if file does not exist, one shall be created
conn = sqlite3.connect(db_name)

# Create the street-gush-helka table
conn.execute(''' CREATE TABLE IF NOT EXISTS street_gush_helka (
                 city_id integer,
                 city_name text,
                 street_id integer,
                 street_name text,
                 building_num text,
                 gush integer,
                 helka integer,
                 PRIMARY KEY (city_id, street_id, building_num)
                 ) ''')

conn.close()



