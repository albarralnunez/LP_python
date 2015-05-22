import urllib
import xml.etree.ElementTree as ET
                  
sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
xmlSource = sock.read()                            
sock.close()

root = ET.fromstring(xmlSource)

a = root.findall("./body/resultat/actes/acte")

for e in a:
    aux = e.findall("./*[nom='la Guineueta']")
    if aux:
        print e