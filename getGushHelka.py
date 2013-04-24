#!/usr/bin/python
#IMPORTS
import urllib
import urllib2
from bs4 import BeautifulSoup
import sys

#FUNCTION
def GetGushHelka(cityid, streetid, houseid):
    """
    Gets cityID, streetID, houseID
    returns a tuple as (GushID,HelkaID)

    Example:
    gh = GetGushHelka(3000, 1053, 1)
    print gh[0]                             #will print 30161
    print "Helka: ", gh[1]         #will print 8
    """
    reqURL = 'http://www.gov.il/firstGov/Templates/MapiNewAddressSearch.aspx?NRMODE=Published&NRNODEGUID=%7b426BD068-836D-4C8F-8F82-A3B92215CCD0%7d&NRORIGINALURL=%2fFirstGov%2fTopNav%2fOfficesAndAuthorities%2fOAUList%2fConstSurvey%2ffirstGovGushcalculator%2f&NRCACHEHINT=Guest'
    urlParams = { 'hiddenInputCityVal': str(cityid),
               'hiddenInputStreetVal': str(streetid),
               'hiddenInputHouseNumberVal': houseid.encode('utf8'),
               '__EVENTTARGET':'lnkBtnSearch',           
               }
    
    data = urllib2.urlopen(reqURL, urllib.urlencode(urlParams)).read()
    soup = BeautifulSoup(data.decode('utf-8'))
    soupResult = soup('table', {'id' : 'gush_parcel_TBL'})
    if soupResult:
        row = soupResult[0].tbody('tr')[1]
        gush = int(row('td')[0].contents[0])
        helka = int(row('td')[1].contents[0])
        return (gush, helka)
    else:
        return None

if __name__ == "__main__":
    args = sys.argv[1:]
    print GetGushHelka(*args)