# add support for classes!!

from bentools import *
import modulePath
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
            
            # for now, definitions of functions within 
            # classes get added to the list without any 
            # reference to their containing classes. 
            # this means that they wont be matched 
            # by any function calls. should either 
            # drop them from analysis or figure out how
            # to add them to the call tree properly 
            # and then add capability to match
            # object instantiation to obj.__init__
            # and obj.method() to obj.method...
            
    return functions

def getImports(root, path):
    importedModules = []
    importedFunctions = []
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for x in node.names:
                module_stub = x.asname if x.asname else x.name
                module_name = modulePath.getModulePath(path,module_stub)
                if module_name: importedModules.append(module_name)
        if isinstance(node, ast.ImportFrom):
            module_stub = node.module
            module_name = modulePath.getModulePath(path,module_stub)
            if module_name:
                for x in node.names:
                    fn_name = x.asname if x.asname else x.name
                    if fn_name=='*':
                        # iterate through package and add all functions
                        pass
                    else:
                        importedFunctions.append([module_name,fn_name])
    return importedModules,importedFunctions

def callMatching(root,path,file,functions):
    importedModules,importedFunctions = getImports(root,path)
#    print("    Imported modules from "+path+'\\'+file)
#    print(importedModules)
#    print("    Imported functions from "+path+'\\'+file)
#    print(importedFunctions)
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
        
    for (ast_root,path,pfile) in ASTs:
        functions = callMatching(ast_root,path,pfile,functions)
        
    #printFunctions(functions)
        
        
        
    
    
    
    
    
    
    
    