import ast

class Query:
    
    def __init__(self, queryStr):
        self.queryStr = queryStr

    def __call__(self,arg):
        return ast.literal_eval(self.queryTree)
