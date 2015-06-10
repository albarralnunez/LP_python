# coding=utf-8
import urllib
import xml.etree.ElementTree as ET
import re
from math import radians, cos, sin, asin, sqrt
from HTML import HTMLrender as HTML
import sys
import ast
import unicodedata
import csv
from operator import itemgetter


def normaliza(text):
    if text:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore') \
            if (type(text) == unicode) \
            else text
    else:
        return ""


def checkActivity(queryLst, activity):
    nom_act = activity.find("./nom").text
    barri = activity.find("./lloc_simple/adreca_simple/barri").text
    if barri is None:
        barri = "Ningun"
    nom_lloc = activity.find("./lloc_simple/nom").text
    if normaliza(queryLst).lower() in (
            normaliza(nom_act).lower() +
            normaliza(barri).lower() +
            normaliza(nom_lloc).lower()):
            return True
    return False


def findActivities(activity, queryLst):
    if type(queryLst) is str:
        return checkActivity(queryLst, activity)
    if type(queryLst) is list:
        return reduce(
            lambda x, y: x or y,
            map(
                lambda x: findActivities(activity, x),
                queryLst
            )
        )
    if type(queryLst) is tuple:
        return reduce(
            lambda x, y: x and y,
            map(
                lambda x: findActivities(activity, x),
                queryLst
            )
        )


def findStations(lat, lon):
    # Stations list
    sock = urllib.urlopen(
                "http://wservice.viabicing.cat/v1/getstations.php?v=1"
            )
    stationsXML = sock.read()
    sock.close()
    stationsTree = ET.fromstring(stationsXML)
    stationsLst = stationsTree.findall("./station")

    freeSlots = []
    haveBikes = []
    for stat in stationsLst:
        x = stat.find("./lat").text
        y = stat.find("./long").text
        x, y, xx, yy = map(float, [x, y, lat, lon])
        dist = haversineDistance(x, y, xx, yy)
        if dist <= 500:
            status = stat.find("./status").text
            if status == 'OPN':
                st = {}
                slots = stat.find("./slots").text
                bikes = stat.find("./bikes").text
                st['street'] = stat.find("./street").text
                # Use regular expresion to clean street
                st['streetNumber'] = stat.find("./streetNumber").text
                st['bikes'] = bikes
                st['slots'] = slots
                st['dist'] = "{:.2f}".format(dist)
                if int(slots) > 0:
                    freeSlots.append(st)
                if int(bikes) > 0:
                    haveBikes.append(st)
    freeSlots.sort(key=lambda st: float(st['dist']))
    haveBikes.sort(key=lambda st: float(st['dist']))
    return {'haveBikes': haveBikes[0:5], 'freeSlots': freeSlots[0:5]}


def findTransportation(lon, lat):
    day_buses = []
    night_buses = []
    metros = []
    # BUS
    ifile = open('data/ESTACIONS_BUS.csv', "r")
    reader = csv.reader(ifile, delimiter=';')
    reader.next()
    for stat in reader:
        st = {'tip': 'BUS'}
        dist = haversineDistance(
            float(lon), float(lat), float(stat[4]), float(stat[5])
        )
        if dist <= 500:
            aux_bus = re.split('-+', stat[6])[1:-1]
            st['dist'] = "{:.2f}".format(dist)
            st['stat'] = aux_bus
            st['lon'] = stat[4]
            st['lat'] = stat[5]
            if stat[3] == 'Day buses':
                day_buses.append(st)
            if stat[3] == 'Night buses':
                night_buses.append(st)
    ifile.close()
    # METRO
    ifile = open('data/TRANSPORTS.csv', "r")
    reader = csv.reader(ifile, delimiter=';')
    reader.next()
    for stat in reader:
        st = {'tip': 'MET/TRAM'}
        dist = haversineDistance(
            float(lon), float(lat), float(stat[4]), float(stat[5])
        )
        if dist <= 500:
            st['dist'] = "{:.2f}".format(dist)
            st['stat'] = re.search(
                        '\(.+[0-9]+,?\)|TRAMVIA BLAU', stat[6]
                    ).group(0).replace('(', '').replace(')', '').split(',')
            st['lon'] = stat[4]
            st['lat'] = stat[5]
            metros.append(st)
    ifile.close()

    day_buses.sort(key=lambda s: float(s['dist']))
    night_buses.sort(key=lambda s: float(s['dist']))
    metros.sort(key=lambda s: float(s['dist']))

    result_aux = []
    if day_buses:
        result_aux.append(day_buses[0])
        day_buses = day_buses[1:]
    if night_buses:
        result_aux.append(night_buses[0])
        night_buses = night_buses[1:]
    if metros:
        result_aux.append(metros[0])
        metros = metros[1:]
    result = (
        (metros[:10])+(night_buses[:10])+(day_buses[:10])
    )
    result.sort(key=lambda s: float(s['dist']))
    r = result_aux+result[:10]
    r.sort(key=lambda s: float(s['dist']))
    return r


def haversineDistance(x, y, xx, yy):
    x, y, xx, yy = map(radians, [x, y, xx, yy])
    lon = x - xx
    lat = y - yy
    aux = sin(lat/2)**2 + cos(y) * cos(yy) * sin(lon/2)**2
    return 2 * asin(sqrt(aux)) * 6371000  # Earth radium in meters


def getActivityData(activitiesLst):
    res = []
    for activity in activitiesLst:
        loc = {}
        act = {}
        act['name'] = activity.find("./nom").text
        act['date'] = activity.find("./data/data_proper_acte").text
        loc['spotName'] = activity.find("./lloc_simple/nom").text
        loc['street'] = activity.find(
            "./lloc_simple/adreca_simple/carrer").text
        loc['streetNum'] = activity.find(
            "./lloc_simple/adreca_simple/numero").text
        loc['district'] = activity.find(
            "./lloc_simple/adreca_simple/districte").text
        loc['city'] = activity.find(
            "./lloc_simple/adreca_simple/municipi").text
        loc['area'] = activity.find(
            "./lloc_simple/adreca_simple/barri").text
        loc['pstCode'] = activity.find(
            "./lloc_simple/adreca_simple/codi_postal").text
        aux = activity.find(
            "./lloc_simple/adreca_simple/coordenades/googleMaps")
        loc['x'] = aux.get('lat')
        loc['y'] = aux.get('lon')
        act['loc'] = loc
        res.append(act)
    return res


def main(argv):
    # test
    # aux = \
    #     "('Pedralbes',['Museu Reial Monestir de Santa Maria de Pedralbes',\
    #      'Jardins del Palau de Pedralbes'])"
    # aux = "['Barceloneta','Corts',('taller','pintura')]"
    aux = "('pintura')"

    if len(argv) == 0:
        argv.append(aux)

    if not argv:
        print 'Empty Input'
        return 2
    else:
        queryStr = argv[0]
        tableFormat = int(argv[1]) if len(argv) == 2 else 0

    queryLst = ast.literal_eval(queryStr)

    #   Activities list
    sock = urllib.urlopen(
        "http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199")
    activitiesXML = sock.read()
    sock.close()
    activitiesTree = ET.fromstring(activitiesXML)

    # activitiesTree = ET.parse('data/activities.xml')  # TESTING

    # Apply query
    activitiesLst = \
        filter(
            lambda x: findActivities(x, queryLst),
            activitiesTree.findall("./body/resultat/actes/acte")
        )

    activities = getActivityData(activitiesLst)

    for activity in activities:
        activity['bikeStations'] = findStations(activity['loc']['x'],
                                                activity['loc']['y'])
        activity['TMBStations'] = findTransportation(activity['loc']['x'],
                                                     activity['loc']['y'])

    print "Number of activities: " + str(len(activities))

    html = HTML(tableFormat, 'activities.html')
    # print html.makeHTML(activities)
    html.printHTMLtoFile(activities)
    html.openHTML()

if __name__ == "__main__":
    main(sys.argv[1:])
