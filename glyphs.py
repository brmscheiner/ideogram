import ast

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

def scrape_functiondata(node, module_name):
    fns = []
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
            fns.append(Fn(node.name,module_name))
    return fns
            
def scrape_importdata(node, fns):
    imports = []
    for node in ast.walk(node):
        if isinstance(node, ast.Import):
            for x in node.names:
                imports.append(x.asname if x.asname else x.name)
        if isinstance(node, ast.ImportFrom):
            module_name = node.module
            for x in node.names:
                fn_name = x.asname if x.asname else x.name
                fns.append(Fn(fn_name,module_name))
    return fns,imports
          
def match_calldata(root, fns, module_name):
    current_fn=None
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
                if current_fn==None:
                    name = "main_shuttle" if nameEqualsMain(root) else "body_code" 
                    current_fn = Fn(name, module_name)
                    fns.append(current_fn)
                if node.func.id in [x.name for x in fns]:
                    current_fn.addCall(node.func.id)
    return fns
    
def getAST(filename):
    with open(filename) as f:
        root = ast.parse(f.read())
    fns = scrape_functiondata(root, filename)
    fns,imports = scrape_importdata(root, fns)
    fns = match_calldata(root, fns, filename)
    return fns

def printfns(fns):
    for fn in fns:
        print()
        print(fn.name)
        print(fn.calls)

def glyphData(filename):
    fns = getAST(filename)
    writeNodes(fns)
    writeLinks(fns)
#    printfns(fns)
    
if __name__== '__main__':
    #filename = getFilename()
    filename = "mandelbrot.py"
    glyphData(filename)