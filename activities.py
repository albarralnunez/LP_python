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
    activities = []
    
    def __init__(self, queryStr):
        queryLst = ast.literal_eval(queryStr)
        # Activities list
        sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
        activitiesXML = sock.read()                            
        sock.close()
        
        activitiesTree = ET.fromstring(activitiesXML)
        activitiesLst = activitiesTree.findall("./body/resultat/actes/acte")
        
        # Apply query
        activitiesLst = __findActivities(activitiesLst, queryLst)
        
        self.activities = __getData(activitiesLst)
    
    def __printActivities(activitiesLst):
        for e in activitiesLst:
            for j in e.findall(".//nom"):
                try: 
                    print j.text
                except :
                    print "__can't print"

    def __findActivities(activitiesLst, queryLst):
        if queryLst:
            if type(queryLst) is str:
                xpath = ".//*[nom='"+queryLst+"']"
                activitiesLstAux = \
                    filter(lambda x: x.findall(xpath), activitiesLst)
                xpath = ".//*[barri='"+queryLst+"']"
                activitiesLstAux += \
                    filter(lambda x: x.findall(xpath), activitiesLst)
                return activitiesLstAux
            if type(queryLst) is list:
                aux = map(
                    lambda x: __findActivities(activitiesLst, x), 
                    queryLst
                )
                return [item for sublist in aux for item in sublist]
            if type(queryLst) is tuple:
                aux = __findActivities(activitiesLst, queryLst[0]) 
                return __findActivities(aux, queryLst[1:])
        return activitiesLst
    
    def __getData(activitiesLst):
        res = []
        for activity in activitiesLst:
            name = activity.find("./nom").text
            loc.spotName = activity.find("./lloc_simple/nom").text
            loc.street = activity.find("./lloc_simple/adreca_simple/carrer").text
            loc.streetNum = activity.find("./lloc_simple/adreca_simple/numero").text
            loc.district = activity.find("./lloc_simple/adreca_simple/districte").text
            loc.city = activity.find("./lloc_simple/adreca_simple/municipi").text
            loc.area = activity.find("./lloc_simple/adreca_simple/barri").text
            loc.pstCode = activity.find("./lloc_simple/adreca_simple/codi_postal").text
            aux = activity.find("./lloc_simple/adreca_simple/coordenades/geocodificacio").text
            loc.coo.x = aux.get(x)
            loc.coo.y = aux.get(y)
            date = activity.find("./data/data_proper_acte").text
            tup = (name, loc, date)
            res.append(tup)
        return res