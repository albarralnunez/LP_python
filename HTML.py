# coding=utf-8
import unicodedata
from subprocess import call


class HTMLrender:

    def __init__(self, forma=0, filee='out.html'):
        self.options = {
            0: 'pretty-table',
            1: 'myTable',
            1: 'myOtherTable'
        }
        self.forma = self.options[forma]
        self.file = filee

    def __normaliza(self, text):
        if text:
            if (type(text) == unicode):
                return unicodedata.normalize(
                    'NFKD', text).encode('ascii', 'ignore')
            else:
                return text
        else:
            return ""

    def __makeBikesStations(self, bikes):
        return "\n".join([
            '''<ul>
              <li>
                Calle: {:s}
              </li>
              <li>
                Num. Calle: {:s}
              </li>
              <li>
                Disponibles: {:s}
              </li>
              <li>
                Espacios: {:s}
              </li>
              <li>
                Distancia: {:s}
              </li>
            </ul>'''.format(
                self.__normaliza(bike['street']),
                self.__normaliza(bike['streetNumber']),
                self.__normaliza(bike['bikes']),
                self.__normaliza(bike['slots']),
                self.__normaliza(bike['dist'])) for bike in bikes])

    def __makeTMBStations(self, tmbs):
        return "\n".join([
            '''<ul>
              <li>
                Parada de: {:s}
              </li>
              <li>
                Lineas: {:s}
              </li>
              <li>
                Distancia: {:s}
              </li>
            </ul>'''.format(
                self.__normaliza(tmb['tip']),
                self.__normaliza(tmb['stat']),
                self.__normaliza(tmb['dist'])) for tmb in tmbs])

    def __makeDirection(self, tmbs):
        return "{:s}, {:s}, nº {:s}, {:s}, {:s}, {:s}, {:s}".format(
            self.__normaliza(tmbs['spotName']),
            self.__normaliza(tmbs['street']),
            self.__normaliza(tmbs['streetNum']),
            self.__normaliza(tmbs['district']),
            self.__normaliza(tmbs['city']),
            self.__normaliza(tmbs['area']),
            self.__normaliza(tmbs['pstCode']))

    def __makeActivities(self, activities):
        return "\n".join([
            '''<tr>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
              <td>
                {:s}
              </td>
            </tr>'''.format(
                self.__normaliza(act['name']),
                self.__normaliza(act['date']),
                self.__makeDirection(act['loc']),
                self.__makeBikesStations(act['bikeStations']['freeSlots']),
                self.__makeBikesStations(act['bikeStations']['haveBikes']),
                self.__makeTMBStations(act['TMBStations'][:5]),
                self.__makeTMBStations(act['TMBStations'][5:]))
            for act in activities])

    def makeHTML(self, activities):
        return '''<!doctype html>
        <html>
        <head>
          <title>Python exercice for LP course</title>
          <style type="text/css">
            .myOtherTable {{ width:400px;background-color:#FFFFE0;border-collapse:collapse;color:#000;font-size:18px; }}
            .myOtherTable th {{ background-color:#BDB76B;color:white;width:50%;font-variant:small-caps; }}
            .myOtherTable td, .myOtherTable th {{ padding:5px;border:0; }}
            .myOtherTable td {{ font-family:Georgia, Garamond, serif;border-bottom:1px solid #BDB76B;height:180px; }}
          </style>
          <style type="text/css">
            .myTable {{ width:1000px;background-color:#eee;border-collapse:collapse; }}
            .myTable th {{ background-color:#000;color:white;width:50%; }}
            .myTable td, .myTable th {{ padding:5px;border:1px solid #000; }}
           </style>
           <link rel="stylesheet" type="text/css" href="pretty-table.css" media="screen" />
        </head>
        <body>
          <table class="{:s}">
            <tr>
              <th>Nombre Actividad</th><th>Hora</th><th>Dirección</th>
              <th>Paradas Bicing con sitios</th><th>Paradas Bicing con bicis</th>
              <th>Transporte  Publico</th>
            </tr>
            {:s}
        </table>
        </body>
        </html>'''.format(
            self.forma,
            self.__makeActivities(activities))

    def printHTMLtoFile(self, activities):
        f = open(self.file, "w")
        f.write(self.makeHTML(activities))

    def openHTML(self):
        call(["run-mailcap", self.file])
