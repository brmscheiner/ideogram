from random import randint

class fn: 
    def __init__(self, identifier, name):
        self.id     = identifier 
        self.name   = name
        self.weight = 0
        self.calls  = dict()
    
    def setWeight(self,weight):
        self.weight = weight 
        
    def increaseWeight(self):
        self.weight += 1

    def addCall(self,called):
        if called in self.calls:
            self.calls[called] += 1
        else: 
            self.calls[called] = 1
            
def genMatrixHeader(fns):
    yield "function_name"
    for fn in fns:
        yield ","+fn.name
    yield "\n"
    
def genMatrixRow(fns,fn):
    yield fn.name
    for ifn in fns:
        if ifn in fn.calls:
            yield ","+str(fn.calls[ifn])
        else: yield ",0"
    yield "\n"
    
def writeMatrix(fns,filename="outputMatrix.csv"):
    f = open(filename,'w')
    f.writelines(genMatrixHeader(fns))
    for fn in fns:
        f.writelines(genMatrixRow(fns,fn))
    f.close()
    
def writeWeights(fns,filename="outputWeights.csv"):
    f = open(filename,'w')
    f.write("function_name,weight\n")
    for fn in fns:
        f.write(fn.name+","+str(fn.weight)+"\n")
    f.close()
    
    
def test():
    n = 15 # number of test functions to create
    fns = [fn(i,str(i)+"_name") for i in range(n)]
    for i in range(n):
        fns[i].setWeight(randint(1,100))
    for i in range(n):
        for j in range(n):
            if randint(0,3) > 1:
                fns[i].addCall(fns[j])
    writeMatrix(fns)
    writeWeights(fns)
    return fns