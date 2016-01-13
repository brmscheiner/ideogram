from random import randint
import sys,ast,os.path

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
    
def scrape_functiondata(node):
    fns = []
    n = 0
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
            fns.append(fn(n,node.name))
            n += 1
    return fns
            
def scrape_calldata(root,fns):
    unprocessed_nodes=[root]
    while unprocessed_nodes != []:
        node = unprocessed_nodes.pop()
        unprocessed_nodes += [i for i in ast.iter_child_nodes(node)]
        if isinstance(node,ast.FunctionDef):
            for fn in fns:
                if fn.name == node.name:
                    current_fn = fn
                    break
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Name):
                if "current_fn" not in locals():
                    if node.func.id == 'main':
                        pass
                    else:
                        print("Call detected before function definition!")
                        print("Function called: "+node.func.id)
                else:
                    if node.func.id in [x.name for x in fns]:
                        current_fn.addCall(node.func.id)
    return fns
    
def getAST(filename):
    f = open(filename)
    root = ast.parse(f.read())
    f.close()
    fns = scrape_functiondata(root)
    fns = scrape_calldata(root,fns)
    for fn in fns:
        print()
        print(fn.name)
        print(fn.calls)
        
if __name__== '__main__':
    #filename = getFilename()
    filename = "mandelbrot.py"
    s = getAST(filename)        