# coding=utf-8

import urllib
import ast
import xml.etree.ElementTree as ET
import re
from math import radians, cos, sin, asin, sqrt
from HTML import HTMLrender as HTML
from activities import Activities

def findStations(stationsLst, coo):
    res = []
    for stat in stationsLst:
        x = stat.find("./lat").text
        y = stat.find("./long").text
        x, y, xx, yy = map(int, [x, y, coo.x, coo.y])
        dist = haversineDistance(x,y,xx,yy)
        if dist <= 500:
            status = station.find("./status").text
            slots = station.find("./slots").text
            if status == 'OPN' and int(slots) > 0:
                street = station.find("./street").text
                #use regular expresion to clean street
                streetNumber = station.find("./streetNumber").text
                bikes = station.find("./bikes").text
                tup = (street, streetNumber, bikes, slots, str(dist))
                res.append(tup)
    return sorted(res, key=lambda tup: tup[4])[0:4]

def haversineDistance(x,y,xx,yy):
    x, y, xx, yy = map(radians, [x, y, xx, yy])
    lon = x - xx 
    lat = y - yy 
    aux = sin(lat/2)**2 + cos(x) * cos(y) * sin(lon/2)**2
    return 2 * asin(sqrt(aux)) * 6371 # Earth radium in Km

def main():

    queryStr = "('Pedralbes',['Museu Reial Monestir de Santa Maria de Pedralbes', 'Jardins del Palau de Pedralbes'])"
    act = Activities(queryStr)
    
    # Stations list
    sock = urllib.urlopen("http://wservice.viabicing.cat/v1/getstations.php?v=1") 
    stationsXML = sock.read()                            
    sock.close()
    stationsTree = ET.fromstring(stationsXML)
    stationsLst = stationsTree.findall("./station")
    
    for activity in act.activities
        activity.stations = findStations(stationsLst, activity.loc.coo)
    
    print stationsLst    

    '''
    html = HTML()
    html.addActivities(activities)
    html.printHTML()
    '''
if __name__ == "__main__":
    main()
