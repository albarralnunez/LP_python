# coding=utf-8
class HTMLrender:
    
    table = []
        
    def printHTML(self):
        print '<!doctype html>'
        print '<html>'
        print '<head>'
        print '  <title>Python exercice for LP course</title>'
        print '  <style type="text/css">'
        print '    .myOtherTable { width:400px;background-color:#FFFFE0;border-collapse:collapse;color:#000;font-size:18px; }'
        print '    .myOtherTable th { background-color:#BDB76B;color:white;width:50%;font-variant:small-caps; }'
        print '    .myOtherTable td, .myOtherTable th { padding:5px;border:0; }'
        print '    .myOtherTable td { font-family:Georgia, Garamond, serif; border-bottom:1px solid #BDB76B;height:180px; }'
        print '  </style>'
        print '</head>'
        print '<body>'
        print '  <table class="myOtherTable">'
        print '    <tr>'
        print '      <th>Table Header</th><th>Table Header</th>'
        print '    </tr>'
        for act in self.table:
            print '    <tr>' 
            print '      <td>'
            print act['name']
            print '      </td>'
            print '      <td>'
            print act['date']
            print '      </td>'
            print '      <td>'
            print act['loc']['spotName']
            print '      </td>'
            print '      <td>'
            print act['loc']['street']
            print '      </td>'
            print '      <td>'
            print act['loc']['streetNum']
            print '      </td>'
            print '      <td>'
            print act['loc']['district']
            print '      </td>'
            print '      <td>'
            print act['loc']['city']
            print '      </td>'
            print '      <td>'
            print act['loc']['area']
            print '      </td>'
            print '      <td>'
            print act['loc']['pstCode']
            print '      </td>'
            print '    </tr>'
        print '</table>'
        print '</body>'
        print '</html>'
    
    def addActivities(self, activities):
        self.table = activities#[('a','a2'),('b','b2'),('c','c2')]