# add support for classes!!

from bentools import *
import ast
import os
from subprocess import call

class Fn: 
    def __init__(self, path, file, name, weight=0):
        self.path    = forcestring(path)
        self.path    = forcestring(file)
        self.name    = forcestring(name)
        self.id      = path+'\\'+file+'  '+name
        self.weight  = weight
        self.calls   = dict()
    
    def setWeight(self,weight):
        self.weight = weight 
        
    def incWeight(self):
        self.weight += 1

    def addCall(self,called):
        if called in self.calls:
            self.calls[called] += 1
        else: 
            self.calls[called] = 1

def getAST(path,file):
    filepath = path+'\\'+file
    try:
        with open(filepath) as f:
            root = ast.parse(f.read())
    except: # if the program wont compile maybe its written for Python 2.x
        try:
            call(["2to3","-w",module.name])
            with open(filepath) as f:
                root = ast.parse(f.read())
        except:
            root = None
            print("File "+filepath+" wont compile! Ignoring...")
    return root
    
def getFns(root,path,file):
    functions = []
    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef):
            functions.append( Fn(path,file,node.name) )
    return functions

def printFunctions(functions):
    for fn in functions:
        print(fn.id)

if __name__== '__main__':
    filepath = "bpl-compyler-master"
    #filepath = "test"
    
    ASTs=[]
    for (path,dirs,files) in os.walk(filepath):
        python_files = [x for x in files if x.endswith('.py')] 
        for pfile in python_files:
            ast_root = getAST(path,pfile)
            if ast_root: ASTs.append((ast_root,path,pfile))
    
    functions = []
    for (ast_root,path,pfile) in ASTs:
        functions += getFns(ast_root,path,pfile)
        
    printFunctions(functions)
        
    
    
    
    
    
    
    
    