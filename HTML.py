# coding=utf-8
import unicodedata

class HTMLrender:
    
    def __init__(self, forma=0):
        self.options = {
            0 : 'myTable',
            1 : 'myOtherTable'
        }
        self.forma = self.options[forma]

    def __normaliza(self, text):
        if text:
            return  unicodedata.normalize('NFKD', text).encode('ascii','ignore') \
            if (type(text) == unicode) \
            else text
        else:
            return ""

    def  __printBikesStations(self, bikes):
        return "".join([
            '''      <ul>
                  <li>
                    Calle: {%s}
                  </li>'
                  <li>
                    Num. Calle: {%s}
                  </li>
                  <li>
                    Disponibles: {%s}
                  </li>
                  <li>
                    Espacios: {%s}
                  </li>
                  <li>
                    Distancia: {%s}
                  </li>
                  </ul>
            ''' % ( self.__normaliza(bike['street']),
                    self.__normaliza(bike['streetNumber']),
                    self.__normaliza(bike['bikes']), 
                    self.__normaliza(bike['slots']),
                    self.__normaliza(bike['dist']))
            for bike in bikes])

    def printHTML(self, activities):
        return '<!doctype html>'
        print '<html>'
        print '<head>'
        print '  <title>Python exercice for LP course</title>'
        print '  <style type="text/css">'
        print '    .myOtherTable { width:400px;background-color:#FFFFE0;border-collapse:collapse;color:#000;font-size:18px; }'
        print '    .myOtherTable th { background-color:#BDB76B;color:white;width:50%;font-variant:small-caps; }'
        print '    .myOtherTable td, .myOtherTable th { padding:5px;border:0; }'
        print '    .myOtherTable td { font-family:Georgia, Garamond, serif; border-bottom:1px solid #BDB76B;height:180px; }'
        print '  </style>'
        print '  <style type="text/css">'
        print '    .myTable { width:1000px;background-color:#eee;border-collapse:collapse; }'
        print '    .myTable th { background-color:#000;color:white;width:50%; }'
        print '    .myTable td, .myTable th { padding:5px;border:1px solid #000; }'
        print '   </style>'
        print '</head>'
        print '<body>'
        print '  <table class="'+self.forma+'">'
        print '    <tr>'
        print '      <th>Table Header</th><th>Table Header</th>'
        print '    </tr>'
        for act in activities:
            print '    <tr>' 
            print '      <td>'
            print self.__normaliza(act['name'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['date'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['spotName'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['street'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['streetNum'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['district'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['city'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['area'])
            print '      </td>'
            print '      <td>'
            print self.__normaliza(act['loc']['pstCode'])
            print '      </td>'
            print '      <td>'
            print self.__printBikesStations(act['bikeStations']['freeSlots'])
            print '      </td>'
            print '      <td>'
            print self.__printBikesStations(act['bikeStations']['haveBikes'])
            print '      </td>'
            #print '      <td>'
            #printMTStations()
            #print '      </td>'
            print '    </tr>'
        print '</table>'
        print '</body>'
        print '</html>'
        
        def printHTMLtoFile(self, activities, file):
            f = open(file,"w")
            f.write(self.printHTML(activities))