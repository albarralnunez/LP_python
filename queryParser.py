import tinytree

class Query:
    
    def __init__(self, queryStr):
        self.queryStr = queryStr
        self.queryTree = Node("root")
        
    def __call__(self,arg):
        self.queryTree = __makeTree(self.queryTree, self.queryStr)
        return 'hello world'
        
    def __makeTree(qTree, qStr):
        if qStr.begin() = '(':
            qStr[1:].span(',')[0]
            
        