#!/usr/bin/python
import getGushHelka
import sys
import sqlite3

if len(sys.argv) != 2:
    print "Usage: %s <dbname>" % sys.argv[0]
    sys.exit(1)

db_name = sys.argv[1]

conn = sqlite3.connect(db_name)

for row in conn.execute('''SELECT city_id, street_id, building_num, street_name, city_name 
                           FROM street_gush_helka
                           WHERE gush is null or helka is null'''):
    city_id = row[0]
    street_id = row[1]
    building_num = row[2]
    print row[0], row[1], row[2], row[3].encode('utf8'), row[4].encode('utf8')
    gushHelka = getGushHelka.GetGushHelka(city_id, street_id, building_num)
    if not gushHelka:
        gushHelka = (-1,-1)
        print "didn't get gush/helka, crap :("
    else:
        print 'got gush/helka:', gushHelka
    
    conn.execute('''update street_gush_helka set gush = ?, helka = ? where
                    city_id = ? and street_id = ? and building_num = ?''', gushHelka + tuple(row[0:3]))
    conn.commit()
    
        

conn.close()


#conn = sqlite3.connect(db_name)
#for row in conn.execute('''SELECT * 
#                           FROM street_gush_helka'''):
#    print row

#conn.close()