# add support for classes!!

from bentools import *
import modulePath
import ast
import os
import json
from subprocess import call

class Fn: 
    def __init__(self, path, file, name, parent_class=None, weight=0):
        self.path     = forcestring(path)
        self.file     = forcestring(file)
        self.name     = forcestring(name)
        self.filepath = path+'\\'+file
        self.id       = path+'\\'+file+'  '+name
        self.weight   = weight
        self.calls    = dict()
        if parent_class:
            forcestring(parent_class)
        self.parent_class = parent_class
    
    def setWeight(self,weight):
        self.weight = weight 
        
    def incWeight(self):
        self.weight += 1
        
    def parentClassStr(self):
        if not self.parent_class:
            return "None."
        return self.parent_class
        
    def isReferenced(self,ast_call,call_path):
        if ast_call.func.id == self.name:
            if call_path == self.path:
                return True
        return False
    
    def isObjectInit(self,ast_call,call_path):
        if self.name != "__init__":
            return False
        if ast_call.func.id == self.parent_class:
            return True
            
    def isModuleObjectInit(self,maybe_module_name,maybe_object_name):
        if self.name != "__init__":
            return False
        if maybe_module_name+".py" == self.file:
            if maybe_object_name == self.parent_class:
                return True
        return False

    def addCall(self,called):
        if called in self.calls:
            self.calls[called] += 1
        else: 
            self.calls[called] = 1
            
    def makeSimpleAttributes(self,filepath_dict,id_dict):
        self.sid       = id_dict[self.id]
        self.sfilepath = filepath_dict[self.filepath]

def printImports(importedModules,importedFunctions,path,file):
    print("    Imported modules from "+path+'\\'+file)
    print(importedModules)
    print("    Imported functions from "+path+'\\'+file)
    print(importedFunctions)
    
def printFunctions(functions):
    for fn in functions:
        print(fn.id)
        print("           Class: "+fn.parentClassStr())

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
    body_code = Fn(path,file,'body_code')
    functions = [body_code]
    
    current_class = None
    before_parent = None
    unprocessed_nodes=[root]
    while unprocessed_nodes != []:
        node = unprocessed_nodes.pop(0)
        if node == before_parent:
            current_class = None
            
        if isinstance(node, ast.ClassDef):
            if unprocessed_nodes:
                before_parent = unprocessed_nodes[0]
            current_class = node.name
            
        unprocessed_nodes = [i for i in ast.iter_child_nodes(node)] + \
                                                            unprocessed_nodes
                                                            
        if isinstance(node, ast.FunctionDef):
            functions.append( Fn(path,file,node.name,current_class) )
            
    # Am I catching one-line function defs, 
    # such as lambda functions and calls to function
    # generators?
            
    return functions

def getImports(root, path, functions):
    importedModules = []
    importedFunctionStrs = []
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for x in node.names:
                module_stub = x.asname if x.asname else x.name
                module_name = modulePath.getModulePath(path,module_stub)
#                if module_name: 
#                    print(module_name+" was FOUND!") 
                if module_name: importedModules.append(module_name)
        if isinstance(node, ast.ImportFrom):
            module_stub = node.module
            module_name = modulePath.getModulePath(path,module_stub)
#            if module_name: 
#                print(module_name+" was FOUND!") 
            if module_name:
                for x in node.names:
                    fn_name = x.asname if x.asname else x.name
                    if fn_name=='*':
                        for fn in functions:
                            if fn.filepath == module_name:
                                function_str_tuple = (module_name,fn.name)
                                importedFunctionStrs.append(function_str_tuple)
                    else:
                        importedFunctionStrs.append((module_name,fn_name))
                        
    importedFunctions = []
    for (module_name,fn_name) in importedFunctionStrs:
        for fn in functions:
            if fn.filepath == module_name:
                if fn.name == fn_name:
                    importedFunctions.append(fn)
                else:
#                    print("No match found for "+fn_name+" in "+module_name)
#                    print("...hopefully an inline function or class definition")
                    pass
    return importedModules,importedFunctions

def nameEqualsMain(root):
    # returns True if file of structure if __name__=='__main__'
    unprocessed_nodes=[root]
    depth=0
    while unprocessed_nodes != [] and depth < 2:
        # if __name__=='__main__' clause occurs at depth=1
        node = unprocessed_nodes.pop()
        unprocessed_nodes += [i for i in ast.iter_child_nodes(node)]
        if isinstance(node, ast.If):
            ifsubnodes = [i for i in ast.iter_child_nodes(node)]
            for i in ifsubnodes:
                if isinstance(i, ast.Compare):
                    leftside   = i.left
                    rightside  = i.comparators[0]
                    if isinstance(leftside, ast.Name):
                        left__name__  = leftside.id=="__name__"
                    if isinstance(rightside, ast.Str):
                        right__main__ = rightside.s=="__main__"
                    if left__name__ and right__main__:
                        return True
                    break
        depth+=1
    return False
    
def callMatching(root,path,file,functions):
    importedModules,importedFunctions = getImports(root,path,functions)
    #printImports(importedModules,importedFunctions,path,file)
    
    n=0
    m=0    
    
    if nameEqualsMain:
        main_shuttle = Fn(path,file,'main_shuttle')
        functions.append(main_shuttle)
        sourceFunction = main_shuttle
    else:
        for fn in functions:
            if fn.name == 'body_code':
                sourceFunction = fn
                break
            
    unprocessed_nodes=[root]
    while unprocessed_nodes != []:
        node = unprocessed_nodes.pop()
        unprocessed_nodes += [i for i in ast.iter_child_nodes(node)]
        processed = False
        
        if isinstance( node, ast.Call ):
            if isinstance( node.func, ast.Name ):
            # calling function inside namespace, i.e. foo(x) or randint(x,y)
                for fn in functions:
                    if fn.isReferenced(node,fn.path):
                        sourceFunction.addCall(fn)
                        processed = True
                        
                    if fn.isObjectInit(node,fn.path):
                        sourceFunction.addCall(fn)
                        processed = True
                        
                if not processed:
                    for fn in importedFunctions:
                        if fn.isReferenced(node,fn.path):
                            sourceFunction.addCall(fn)
                            processed = True
        
            elif isinstance( node.func, ast.Attribute):
            # calling function outside namespace, exe. random.randint(x,y)
                try:
                    target_module   = node.func.value.id
                    target_function = node.func.attr
                    
                    
                    for iMod in importedModules:
                        for fn in functions:
                            if iMod == fn.filepath:
                                if target_function == fn.name:
                                    sourceFunction.addCall(fn)
                                    processed = True
                                    break
                                    
                    if not processed:
                        for fn in functions:
                            if fn.name == target_function: 
                            # is it an object method?
                                sourceFunction.addCall(fn)
                                processed = True
                                break
                            if fn.isModuleObjectInit(target_module,target_function):
                            # is it an object init from a class defined in 
                            # another module?
                                sourceFunction.addCall(fn)
                                processed = True
                                break
                                
                except AttributeError:
#                    print("Import statement unusable..")
#                    print(ast.dump(node))
                    pass
            
            if processed: n+=1
            if not processed:
                m += 1

    print(path+'\\'+file)   
    print(str(n)+" calls processed, "+str(m)+" calls not processed.")
    print()
    return functions

def addSimpleAttributes(functions):
    i=0
    j=0
    id_dict = dict()
    filepath_dict = dict()
    for fn in functions:
        sid = 'f'+str(i)
        i += 1
        id_dict[fn.id]=sid
        if fn.filepath in filepath_dict.keys():
            sfilepath = filepath_dict[fn.filepath]
        else:
            sfilepath = j
            j += 1
            filepath_dict[fn.filepath] = j
        fn.makeSimpleAttributes(filepath_dict,id_dict)
    return functions

def writeJSON(functions,outfile="d3js\\out.json"):
    data = dict()
    nodelist = []
    for fn in functions:
        node = dict()
        node["id"]   = fn.sid
        node["file"] = fn.sfilepath
        nodelist.append(node)
    data["nodes"] = nodelist
    linklist = []
    for fn in functions:
        if len(fn.calls) > 0:
            for key in fn.calls:
                link = dict()
                link["source"] = int(fn.sid[1:])
                link["target"] = int(key.sid[1:])
                link["value"]  = fn.calls[key]
                linklist.append(link)
    data["links"] = linklist
    with open(outfile, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return

if __name__== '__main__':
    filepath = "test\\demo"
    
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
    functions = addSimpleAttributes(functions)
    writeJSON(functions)
        
        
        
    
    
    
    
    
    
    
    