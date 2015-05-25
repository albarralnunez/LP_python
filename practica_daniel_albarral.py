# coding=utf-8
import urllib
import xml.etree.ElementTree as ET
import re
from math import radians, cos, sin, asin, sqrt
from HTML import HTMLrender as HTML
from activities import Activities
import sys

def findStations(stationsLst, lat, lon):
    res = []
    for stat in stationsLst:
        st = {}
        x = stat.find("./lat").text
        y = stat.find("./long").text
        x, y, xx, yy = map(float, [x, y, lat, lon])
        dist = haversineDistance(x,y,xx,yy)
        if dist <= 0.5:
            status = stat.find("./status").text
            slots = stat.find("./slots").text
            if status == 'OPN' and int(slots) > 0:
                st['street'] = stat.find("./street").text
                #use regular expresion to clean street
                st['streetNumber'] = stat.find("./streetNumber").text
                st['bikes'] = stat.find("./bikes").text
                st['slots'] = slots
                st['dist'] = str(dist)
                res.append(st)
    return sorted(res, key=lambda st: st['dist'])[0:4]

def haversineDistance(x,y,xx,yy):
    x, y, xx, yy = map(radians, [x, y, xx, yy])
    lon = x - xx 
    lat = y - yy 
    aux = sin(lat/2)**2 + cos(x) * cos(y) * sin(lon/2)**2
    return 2 * asin(sqrt(aux)) * 6371 # Earth radium in Km

def main(argv):

    aux = "('Pedralbes',['Museu Reial Monestir de Santa Maria de Pedralbes', 'Jardins del Palau de Pedralbes'])"
    queryStr = aux#argv[0]
    tableFormat = int(argv[1]) if len(argv)==2 else 0
    
    if not queryStr:
        print 'Empty Input'
        return 2
    try:
        act = Activities(queryStr)
    except:
        print 'Invalid input'
        return 2
    # Stations list
    sock = urllib.urlopen("http://wservice.viabicing.cat/v1/getstations.php?v=1") 
    stationsXML = sock.read()                            
    sock.close()
    stationsTree = ET.fromstring(stationsXML)
    stationsLst = stationsTree.findall("./station")
    
    for activity in act.activities:
        activity['stations'] = findStations(stationsLst, activity['loc']['x'], activity['loc']['y'])

    html = HTML(tableFormat)
    html.printHTML(act.activities)

if __name__ == "__main__":
    main(sys.argv[1:])
