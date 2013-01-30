import re
import urllib2
import time

"""
This file is a script that is supposed to get an array of streets
    and their known building numbers
"""

#CONSTANTS
GET_STREET_BY_CITY_ID_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getStreets?cityNum="
GET_STREET_NUMBERS_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getNumbers?streetCode="
JERUSALEM_ID = 3000

def getCityIDS():
    """
    Returns an array of tuples of the form (CITY_ID,CITY_NAME) of all the cities
    """
    gushHelkaResponse = urllib2.urlopen("http://www.gov.il/FirstGov/TopNav/OfficesAndAuthorities/OAUList/ConstSurvey/firstGovGushcalculator/").read()
    CITY_ID_REGEX = '<option value=\"(\d+)\">(.*?)</option>'
    cityArr = re.findall(CITY_ID_REGEX,gushHelkaResponse)
    return  cityArr

def getStreetsArrOfCity(cityID):
    """
    Gets an ID of a city
    Returns an array of tuples of the form (STREET_ID,STREET_NAME)

    Example:
    getStreetsArrOfCity(3000)
    [(1,'Ben-Yehuda'),(2,'King Geroge'),...]
    """
    jerusalemStreetsResponse = urllib2.urlopen(GET_STREET_BY_CITY_ID_REQ+str(cityID)).read()
    STREET_ID_REGEX = '<street id=\"(\d+)\"><name>(.*?)</name></street>'
    streetsArr = re.findall(STREET_ID_REGEX,jerusalemStreetsResponse)
    return streetsArr

def getStreetNumbersResponse(url,tryNum=0,maxTries = 5):
    """
    gets the request from the given url
    if it fails, it waits 0.5 secs and tries again for MAX_TRIES
    """
    if tryNum > maxTries:
        raise LookupError("Connection could not be made to "+str(url))
    try:
        retStr = urllib2.urlopen(url).read()
        return retStr
    except:
        time.sleep(0.05)
        tryNum = tryNum+1
        return getStreetNumbersResponse(url,tryNum)

def getCityStreetBuildingNumsArr(cityID):
    """
    Gets a cityID
    Returns an array of tuples of the form (streetID,streetName,arrOfBuildings)
        where arrOfBuildings is an array of the building nums (as strings) that are known
    """
    streetsOfCity = getStreetsArrOfCity(cityID)
    streetsArr = []
    STREET_NUM_REGEX = '<number>(.*?)</number>'
    counter= 0
    for street in streetsOfCity:
        responseXML = getStreetNumbersResponse(GET_STREET_NUMBERS_REQ+str(street[0]),1)
        numberStreetArr = re.findall(STREET_NUM_REGEX,responseXML)
        newStreet = (street[0],street[1],numberStreetArr)
        streetsArr.append(newStreet)
        counter = counter +1
        if counter % 50 == 0:
            print "Got "+str(counter)+" streets!"
    return streetsArr

    #streetsArr finishes with an array of tuples of all the streets with their IDs and house numbers