import re
import urllib2

GET_STREET_BY_CITY_ID_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getStreets?cityNum="
GET_STREET_NUMBERS_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getNumbers?streetCode="
JERUSALEM_ID = 3000

jerusalemStreetsResponse = urllib2.urlopen(GET_STREET_BY_CITY_ID_REQ+str(JERUSALEM_ID)).read()

STREET_ID_REGEX = '<street id=\"(\d+)\"><name>(.*?)</name></street>'
primaryStreetsArr = re.findall(STREET_ID_REGEX,jerusalemStreetsResponse)

streetsArr = []
STREET_NUM_REGEX = '<number>(.*?)</number>'
for street in primaryStreetsArr:
    responseXML = urllib2.urlopen(GET_STREET_NUMBERS_REQ+str(street[0])).read()
    numberStreetArr = re.findall(STREET_NUM_REGEX,responseXML)
    newStreet = (street[0],street[1],numberStreetArr)
    streetsArr.append(newStreet)

#streetsArr finishes with an array of tuples of all the streets with their IDs and house numbers