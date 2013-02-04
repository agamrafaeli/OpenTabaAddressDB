# -*- coding: UTF-8-*-

#IMPORTS
import re
import urllib2
import time

"""
This file is a script that is supposed to get the info
    of cities, streets and building nums all over Israel
"""

#CONSTANTS
GUSH_HELKA_CALCULATOR_URL = "http://www.gov.il/FirstGov/TopNav/OfficesAndAuthorities/OAUList/ConstSurvey/firstGovGushcalculator/"
GET_STREET_BY_CITY_ID_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getStreets?cityNum="
GET_STREET_NUMBERS_REQ = "http://www.gov.il/firstgov/services/MapiInformation.aspx/getNumbers?streetCode="

#REGEXS
STREET_ID_REGEX = '<street id=\"(\d+)\"><name>(.*?)</name></street>'
CITY_ID_REGEX = '<option value=\"(\d+)\">(.*?)</option>'
STREET_NUM_REGEX = '<number>(.*?)</number>'

def getCities():
    """
    Returns an array of tuples of the form (CITY_ID,CITY_NAME) of all the cities
    """
    gushHelkaResponse = urllib2.urlopen(GUSH_HELKA_CALCULATOR_URL).read()
    cityArr = re.findall(CITY_ID_REGEX,gushHelkaResponse)
    return  cityArr

def getStreetsByCity(city):
    """
    Gets an ID of a city
    Returns an array of tuples of the form (STREET_ID,STREET_NAME)

    Example:
    getStreetsArrOfCity(3000)
    [(1,'Ben-Yehuda'),(2,'King Geroge'),...]
    """
    streetsResponse = urllib2.urlopen(GET_STREET_BY_CITY_ID_REQ+str(city)).read()
    streetsArr = re.findall(STREET_ID_REGEX,streetsResponse)
    return streetsArr

def getBuildingNumsByStreet(street):
    """
    Gets an ID of a Street
    Returns an array of all the building numbers of that street

    Example:
    getBuildingNumsByStreet(1567)
    ['1','2','3-8']
    """
    responseXML = urllib2.urlopen(GET_STREET_NUMBERS_REQ+str(street)).read()
    buildingNums = re.findall(STREET_NUM_REGEX,responseXML)
    return buildingNums
