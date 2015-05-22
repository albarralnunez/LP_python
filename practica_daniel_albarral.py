import urllib
import ast
import xml.etree.ElementTree as ET

def findActiviteis(activitiesLst, queryLst):
    queryParam = queryLst[0]
    if type(queryParam) is str:
        for activiti in activitiesLst
            xpath = "./*[nom='+"+queryParam+"']"
            e.findall(xpath)
            
        findActiviteis(activitiesLst, queryLst.remove(0))
    if type(queryParam) is tuple
        findActiviteis(activitiesLst, queryLst[0])


def main():
    queryStr = "('taller','horta',['musica','pintura'])"
    queryLst = ast.literal_eval(a)
    
    # Activities list
    sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
    activitiesXML = sock.read()                            
    sock.close()
    activitiesTree = ET.fromstring(activitiesXML)
    activitiesLst = activitiesTree.findall("./body/resultat/actes/acte")
    
    # Apply query
    activitiesLst = findActiviteis(activitiesLst, queryLst)

if __name__ == "__main__":
    main()
