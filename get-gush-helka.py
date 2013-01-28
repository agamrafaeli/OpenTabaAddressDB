#!/usr/bin/python
import re
import urllib
import urllib2

import HTMLParser
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def GetGushHelka(cityid, streetid, houseid):
    addr = 'http://www.gov.il/firstGov/Templates/MapiNewAddressSearch.aspx?NRMODE=Published&NRNODEGUID=%7b426BD068-836D-4C8F-8F82-A3B92215CCD0%7d&NRORIGINALURL=%2fFirstGov%2fTopNav%2fOfficesAndAuthorities%2fOAUList%2fConstSurvey%2ffirstGovGushcalculator%2f&NRCACHEHINT=Guest'
    
    params = { 'hiddenInputCityVal': str(cityid),
               'hiddenInputStreetVal': str(streetid),
               'hiddenInputHouseNumberVal': str(houseid),
               '__EVENTTARGET':'lnkBtnSearch',           
               }
    
    data = urllib2.urlopen(addr, urllib.urlencode(params)).read()
    soup = BeautifulSoup(data.decode('utf-8'))
    soup = BeautifulSoup(data.decode('utf-8'))
    row = soup('table', {'id' : 'gush_parcel_TBL'})[0].tbody('tr')[1]
    gush = int(row('td')[0].contents[0])
    helka = int(row('td')[1].contents[0])
    
    return (gush, helka)

gh = GetGushHelka(3000, 1053, 1)

print "Gush: ", gh[0]
print "Helka: ", gh[1]

