# coding=utf-8
import csv
import re

class Transportation:
    
    def __init__(self, lon, lat):

        def haversineDistance(x,y,xx,yy):
            x, y, xx, yy = map(radians, [x, y, xx, yy])
            lon = x - xx 
            lat = y - yy 
            aux = sin(lat/2)**2 + cos(x) * cos(y) * sin(lon/2)**2
            return 2 * asin(sqrt(aux)) * 6371000 # Earth radium in Km

        day_buses = []
        night_buses = []
        metro = []
        
        #BUS
        ifile  = open('data/ESTACIONS_BUS.csv', "r")
        reader = csv.reader(ifile, delimiter='\t')
        for stat in reader[1:]:
            dist = haversineDistance(lon,lat,stat[7],stat[8])
            if dist <= 0.5:
                aux_bus = re.split('-+',stat[10])[1:-1]
                st['dist'] = dist
                st['buses'] = aux_bus
                st['lon'] = stat[7]
                st['lon'] = stat[8]
                if stat[5] == 'Day buses':
                    day_buses.apend(st)
                if stat[5] == 'Night buses':
                    night_buses.apend(st)
        ifile.close()
        
        #METRO
        ifile  = open('data/TRANSPORTS.csv', "r")
        reader = csv.reader(ifile, delimiter='\t')
        for stat in reader[1:]:
            dist = haversineDistance(lon,lat,stat[4],stat[5])
            if dist <= 500:
                st['dist'] = str('%.2f' % dist)
                st['metros'] = stat[6]
                st['lon'] = stat[4]
                st['lon'] = stat[5]
                metros.apend(st)
        ifile.close()
        
        sorted(day_buses, key=lambda s: s['dist'])[0:10] 
        sorted(night_buses, key=lambda s: s['dist'])[0:10] 
        sorted(metro, key=lambda s: s['dist'])[0:10]
        self.TMBStations = day_buses
