# coding=utf-8
import ast
import xml.etree.ElementTree as ET
import time
import urllib
import unicodedata

class Activities:
    
    '''
    List of activities tuples, each tuple contains:
        name as str, location as obj and date as str- In this order
    location is a object with this atributes:
        spotName
        street
        streetNum
        district
        city
        area
        pstCode
        coo.x
        coo.y
    '''
    def __normaliza(self, text):
        if (type(text) == unicode):
                text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        return text

    def __init__(self, queryStr):
        
        def checkActivity(queryLst, activity):
            nom_act = activity.find("./nom").text
            barri = activity.find("./lloc_simple/adreca_simple/barri").text 
            if barri is None:
                barri = "Ningun"
            nom_lloc = activity.find("./lloc_simple/nom").text
            #print "</br>"
            #print self.__normaliza(queryLst).lower() + " ->"
            #print self.__normaliza(barri).lower()
            #print "</br>"
            if self.__normaliza(queryLst).lower() in  \
                (self.__normaliza(nom_act).lower() + \
                self.__normaliza(barri).lower() + \
                self.__normaliza(nom_lloc).lower()):
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

        #def findActivities(activity, queryLst):
        #    if queryLst:
        #        if type(queryLst) is str:
        #            return filter ( 
        #                lambda x :checkActivity(queryLst, x), \
        #                activitiesLst
        #            )
        #        if type(queryLst) is list:
        #            aux = map(
        #                lambda x: findActivities(activitiesLst, x), 
        #                queryLst
        #            )
        #            return [item for sublist in aux for item in sublist]
        #        if type(queryLst) is tuple:
        #            aux = findActivities(activitiesLst, queryLst[0]) 
        #            return findActivities(aux, queryLst[1:])
        #    return activitiesLst

        def getData(activitiesLst):
            res = []
            for activity in activitiesLst:
                loc = {}
                act = {}
                act['name'] = activity.find("./nom").text
                act['date'] = activity.find("./data/data_proper_acte").text
                loc['spotName'] = activity.find("./lloc_simple/nom").text
                loc['street'] = activity.find("./lloc_simple/adreca_simple/carrer").text
                loc['streetNum'] = activity.find("./lloc_simple/adreca_simple/numero").text
                loc['district'] = activity.find("./lloc_simple/adreca_simple/districte").text
                loc['city'] = activity.find("./lloc_simple/adreca_simple/municipi").text
                loc['area'] = activity.find("./lloc_simple/adreca_simple/barri").text
                loc['pstCode'] = activity.find("./lloc_simple/adreca_simple/codi_postal").text
                aux = activity.find("./lloc_simple/adreca_simple/coordenades/googleMaps")
                loc['x'] = aux.get('lat')
                loc['y'] = aux.get('lon')
                act['loc'] = loc
                res.append(act)
            return res

        queryLst = ast.literal_eval(queryStr)
        #   Activities list
        sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
        activitiesXML = sock.read()                            
        sock.close()
        activitiesTree = ET.fromstring(activitiesXML)
        
        #activitiesTree = ET.parse('data/activities.xml') # TESTING

        # Apply query
        t1 = time.clock()
        activitiesLst = \
            filter(
                lambda x: findActivities(x, queryLst), 
                activitiesTree.findall("./body/resultat/actes/acte")
            )
        t2 = time.clock()
        print "Time to find activities: " + str(t2-t1)
        print "</br>"
        self.activities = getData(activitiesLst)

#def printActivities(activitiesLst):
#    for e in activitiesLst:
#        for j in e.findall(".//nom"):
#            try: 
#                print j.text
#            except :
#                print "__can't print"