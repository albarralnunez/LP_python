import urllib
import ast

a = "('taller','horta',['musica','pintura'])"
print ast.literal_eval(a)[0]

'''
sock = urllib.urlopen("http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199") 
xmlSource = sock.read()                            
sock.close()
print xmlSource
'''