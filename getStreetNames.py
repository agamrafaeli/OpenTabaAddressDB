import re
import urllib2
import time

#CONSTANTS
GET_STREET_BY_CITY_ID_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getStreets?cityNum="
GET_STREET_NUMBERS_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getNumbers?streetCode="
JERUSALEM_ID = 3000

#STREETS ARR
jerusalemStreetsResponse = urllib2.urlopen(GET_STREET_BY_CITY_ID_REQ+str(JERUSALEM_ID)).read()
STREET_ID_REGEX = '<street id=\"(\d+)\"><name>(.*?)</name></street>'
primaryStreetsArr = re.findall(STREET_ID_REGEX,jerusalemStreetsResponse)

MAX_TRIES = 5
def getStreetNumbersResponse(url,tryNum):
    """
    gets the request from the given url
    if it fails, it waits 0.5 secs and tries again for MAX_TRIES
    """
    if tryNum > MAX_TRIES:
        raise LookupError("Connection could not be made to "+str(url))
    try:
        retStr = urllib2.urlopen(url).read()
        return retStr
    except:
        time.sleep(0.5)
        return getStreetNumbersResponse(url,tryNum+1)

streetsArr = []
STREET_NUM_REGEX = '<number>(.*?)</number>'
for street in primaryStreetsArr:
    responseXML = getStreetNumbersResponse(GET_STREET_NUMBERS_REQ+str(street[0]),1)
    numberStreetArr = re.findall(STREET_NUM_REGEX,responseXML)
    newStreet = (street[0],street[1],numberStreetArr)
    streetsArr.append(newStreet)

#streetsArr finishes with an array of tuples of all the streets with their IDs and house numbers