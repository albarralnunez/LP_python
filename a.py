import urllib
a = "('taller','horta',['musica','pintura'])"
print a[1:]

sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
xmlSource = sock.read()                            
sock.close()
print xmlSource