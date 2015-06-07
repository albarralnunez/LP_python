# coding=utf-8
import unicodedata
from subprocess import call


class HTMLrender:

    def __init__(self, forma=0, filee='out.html'):
        self.options = {
            0: 'myTable',
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
        return "".join([
            '''<ul>
              <li>
                Calle: {:s}
              </li>'
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
            </ul>
            '''.format(
                self.__normaliza(bike['street']),
                self.__normaliza(bike['streetNumber']),
                self.__normaliza(bike['bikes']),
                self.__normaliza(bike['slots']),
                self.__normaliza(bike['dist'])) for bike in bikes])

    def __makeActivities(self, activities):
        return "".join([
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
            </tr>
            '''.format(
                self.__normaliza(act['name']),
                self.__normaliza(act['date']),
                self.__normaliza(act['loc']['spotName']),
                self.__normaliza(act['loc']['street']),
                self.__normaliza(act['loc']['streetNum']),
                self.__normaliza(act['loc']['district']),
                self.__normaliza(act['loc']['city']),
                self.__normaliza(act['loc']['area']),
                self.__normaliza(act['loc']['pstCode']),
                self.__makeBikesStations(act['bikeStations']['freeSlots']),
                self.__makeBikesStations(act['bikeStations']['haveBikes']))
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
        </head>
        <body>
          <table class="{:s}">
            <tr>
              <th>Table Header</th><th>Table Header</th>
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
