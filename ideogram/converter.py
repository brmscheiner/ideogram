import ast
from printing import printFnDefs
from importAnalysis import getModulePath
from importAnalysis import getImportFromModule
from importAnalysis import getImportFromFn
from importAnalysis import getImportModule
import copy

def show(node):
    ast.dump(node)

def isImport(node):
    pass

def getCurrentClass(stack):
    for x in stack:
        if isinstance(x, ast.ClassDef):
            return x
    return None

def getSourceFnDef(stack,fdefs,path):
    found = False
    for x in stack:
        if isinstance(x, ast.FunctionDef):
            for y in fdefs[path]:
                if ast.dump(x)==ast.dump(y):
                    found = True
                    return y
            raise
    if not found:
        for y in fdefs[path]:
            if y.name=='body':
                return y
    raise
    
def getTargetFnDef(fdefs):
    return None

def calcFnWeight(node):
    '''Calculates the weight of a function definition by recursively counting 
    its child nodes in the AST. Note that the tree traversal will become 
    O(n^2) instead of O(n) if this feature is enabled.'''
    stack = [node]
    count = 0
    while len(stack) > 0:
        node = stack.pop()
        children = [x for x in ast.iter_child_nodes(node)]
        count += len(children)
        stack = stack + children
    return count
                
def traversal(root):
    '''For each subtree, evaluate the deepest nodes first. Then evaluate the
    next-deepest nodes and move on to the next subtree.'''
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if hasattr(node,'children'):
            if node.children == set():
                try:
                    stack[-1].children.remove(node)
                except:
                    pass
                yield (node,stack)
            else:
                childnode = node.children.pop()
                stack += [node,childnode]
        else: 
            children = [x for x in ast.iter_child_nodes(node)]
            node.children = set(children)
            stack.append(node)

def firstPass(ASTs,project_path):
    '''Populate dictionary of function definition nodes, dictionary of imported  
    function names and list of imported module names.'''
    fdefs=dict()
    imp_funcs=dict()
    imp_mods=[]
    for (root,path) in ASTs:
        fdefs[path] = []
        body        = root
        body.name   = "body"
        body.weight = calcFnWeight(body)
        body.path   = path
        body.pclass = None
        fdefs[path].append(body)
        for (node,stack) in traversal(root):
            if isinstance(node,ast.FunctionDef):
                #node.name is already defined by AST module
                node.weight = calcFnWeight(node)
                node.path   = path
                node.pclass = getCurrentClass(stack)
                fdefs[path].append(node)
            elif isinstance(node,ast.ImportFrom):
                module = getImportFromModule(node)
                name   = getImportFromFn(node)
                imp_funcs[module] = name
            elif isinstance(node,ast.Import):
                module = getImportModule(node,path)
                imp_mods.append(module)
    return fdefs,imp_funcs,imp_mods

def secondPass(ASTs,fdefs):
    calls=[]
    for (root,path) in ASTs:
        for (node,stack) in traversal(root):
            if isinstance(node, ast.Call):
                node.source = getSourceFnDef(stack,fdefs,path)
                calls.append(node)
    return calls

def convert(ASTs,project_path):
    copy_ASTs = copy.deepcopy(ASTs)
    print("Making first pass..")
    fdefs,imp_funcs,imp_mods = firstPass(ASTs,project_path)
    print(imp_mods)
    #printFnDefs(fdefs)
    print("Making second pass..")
    calls = secondPass(copy_ASTs,fdefs)








