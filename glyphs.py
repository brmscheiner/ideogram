# weight nodes... based on number of AST children?
# add support for .foo and . import statements
# refactor so function names are unique (use path) 
import ast
import os
from subprocess import call

class Module:
    def __init__(self, path, file):
        self.path        = path
        self.file        = file
        self.name        = path+"\\"+file
        self.callTree    = []

    def addFns(self,invar):
        # Accepts a single function or a list of functions
        if isinstance(invar,Fn):
            self.callTree.append(invar)
        elif isinstance(invar,list):
            for i in invar:
                if isinstance(i,Fn):
                    self.callTree.append(i)
                else: 
                    raise "AAAAAAAGHHHHHHHHH"
        else:
            raise "AAAAAAAGHHHHHHHHH"

class Fn: 
    def __init__(self, name, module, weight=0):
        self.name    = name
        self.weight  = weight
        self.module  = module
        self.calls   = dict()
    
    def setWeight(self,weight):
        self.weight = weight 
        
    def increaseWeight(self):
        self.weight += 1

    def addCall(self,called):
        if called in self.calls:
            self.calls[called] += 1
        else: 
            self.calls[called] = 1
            
def genNodes(fns):
    yield "function_name,weight"
    for fn in fns:
        yield "\n"+fn.name+","+str(fn.weight)
    yield "\n"
    
def genLinks(fns):
    yield "source,target,value\n"
    for source_fn in fns:
        for target_fn in source_fn.calls:
            yield source_fn.name+","+target_fn+","+ \
                  str(source_fn.calls[target_fn])+"\n"
    
def writeNodes(fns,filename="d3js/nodes.csv"):
    with open(filename,'w') as f:
        f.writelines(genNodes(fns))
    
def writeLinks(fns,filename="d3js/links.csv"):
    with open(filename,'w') as f:
        f.writelines(genLinks(fns))

def nameEqualsMain(root):
    # returns True if file of structure if __name__=='__main__'
    # note: what about cases where if __name__=='__main__': main()?
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

def scrape_imports(node, module):
    imported_modules = []
    fns = []
    for node in ast.walk(node):
        if isinstance(node, ast.Import):
            for x in node.names:
                imported_modules.append(x.asname if x.asname else x.name)
        if isinstance(node, ast.ImportFrom):
            new_module_name = node.module
            for x in node.names:
                fn_name = x.asname if x.asname else x.name
                fns.append( Fn(fn_name, new_module_name) )
    module.addFns(fns)
    return imported_modules

def scrape_functiondefs(node, module):
    fns = []
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
            fns.append( Fn(node.name,module.name) )
    module.addFns(fns)
    return 
          
def match_calldata(root, module, modules):
    current_fn=None
    unprocessed_nodes=[root]
    while unprocessed_nodes != []:
        node = unprocessed_nodes.pop()
        unprocessed_nodes += [i for i in ast.iter_child_nodes(node)]
        if isinstance( node, ast.FunctionDef ):
            for fn in module.callTree:
                if fn.name == node.name:
                    current_fn = fn
                    break
        if isinstance( node, ast.Call ):
            print(ast.dump(node))
            if isinstance( node.func, ast.Name ):
                # calling function inside namespace, i.e. foo(x) or randint(x,y)
                if current_fn==None:
                    name = "main_shuttle" if nameEqualsMain(root) else "body_code" 
                    current_fn = Fn(name, module.name)
                    module.addFns(current_fn)
                if node.func.id in [x.name for x in module.callTree]:
                    current_fn.addCall(node.func.id)

            if isinstance( node.func, ast.Attribute ): 
                # calling function outside namespace, exe. random.randint(x,y)
                module_name = node.func.value.id 
                function_name = node.func.attr 
                for mod in modules:
                    if module_name == mod.file:
                        for jfn in mod.callTree:
                            if function_name == jfn.name:
                                current_fn.addCall(function_name)
                                #### refactor tomorrow
                                break
                        new_function = Fn(function_name,mod)
                        mod.addFns(new_function)
                        
                
                    # find function within module and add use .addCall method
                    
                else: # probably in stdlib!
                    # if it's in the subfolders...
                    print(node.func.attr)
                #modules.append(newModule)
                #modules.addFns(thisfn)
                
                
    return
    
def addCallTrees(modules):
    for module in modules:
        print(module.name)
        try:
            with open(module.name) as f:
                ast_root = ast.parse(f.read())
        except: # if the program wont compile because its written for Python 2.x
            try:
                call(["2to3","-w",module.name])
                with open(module.name) as f:
                    ast_root = ast.parse(f.read())
            except:
                print("File "+module.name+" wont compile! Ignoring...")
        imported_modules = scrape_imports(ast_root, module) # modifies module!
        scrape_functiondefs(ast_root, module)
        match_calldata(ast_root, module, modules)
    return modules

def printModules(modules):
    for module in modules:
        print("========")
        print(module.name)
        for fn in module.callTree:
            print("--------")
            print("  "+fn.name)
            for each in fn.calls:
                print("    "+each)
            print(len(module.callTree))
    
if __name__== '__main__':
    #filepath = "bpl-compyler-master"
    filepath = "test"
    modules = []
    for (path,dirs,files) in os.walk(filepath):
        python_files = [x for x in files if x.endswith('.py')] 
        for file in python_files:
            current_module = Module(path,file)
            modules.append(current_module)
    addCallTrees(modules)
    #printModules(modules)
    
    
    