import ast
from printing import printFnDefs
from printing import printImpFuncStrs
from printing import printImpClassStrs
from printing import printImpFuncs
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
    '''VERY VERY SLOW'''
    found = False
    for x in stack:
        if isinstance(x, ast.FunctionDef):
            for y in fdefs[path]:
                if ast.dump(x)==ast.dump(y): #probably causing the slowness
                    found = True
                    return y
            raise
    if not found:
        for y in fdefs[path]:
            if y.name=='body':
                return y
    raise
    
def getTargetFnDef(node,path,fdefs,imp_funcs,imp_mods):
    '''Need to go back through and compare parent classes.
    Also, what about method calls like hat.compare(sombrero)'''
    #CASE 1: calling function inside namespace, like foo(x) or randint(x,y)
    if isinstance(node.func,ast.Name):
        if path in fdefs:
            for x in fdefs[path]:
                if node.func.id == x.name:
                    return x
        if path in imp_funcs:
            for x in imp_funcs[path]:
                if node.func.id == x.name:
                    return x
        return None
    # CASE 2: # calling function outside namespace, like random.randint(x,y)
    elif isinstance(node.func,ast.Attribute):
        try:
            module   = node.func.value.id
            fn_name  = node.func.attr
        except AttributeError:
            return None
        if module in imp_mods[path] and module in fdefs:
            print("inhere")
            for x in fdefs[module]:
                if x.name == fn_name:
                    return x
       # print(module+"    "+fn_name)
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

def formatBodyNode(root,path):
    '''Format the root node for use as the body node.'''
    body        = root
    body.name   = "body"
    body.weight = calcFnWeight(body)
    body.path   = path
    body.pclass = None
    return body

def formatFunctionNode(node,path,stack):
    '''Add some helpful attributes to node.'''
    #node.name is already defined by AST module
    node.weight = calcFnWeight(node)
    node.path   = path
    node.pclass = getCurrentClass(stack)
    return node

def firstPass(ASTs):
    '''Populate dictionary of function definition nodes, dictionary of imported  
    function names and dictionary of imported module names. All three 
    dictionaries use source file paths as keys.'''
    fdefs=dict()
    imp_func_strs=dict()
    imp_mods=dict()
    for (root,path) in ASTs:
        fdefs[path] = []
        fdefs[path].append(formatBodyNode(root,path))
        imp_func_strs[path] = []
        imp_mods[path] = []
        for (node,stack) in traversal(root):
            if isinstance(node,ast.FunctionDef):
                fdefs[path].append(formatFunctionNode(node,path,stack))
            elif isinstance(node,ast.ImportFrom):
                module = getImportFromModule(node,path)
                if module:
                    fn_name = getImportFromFn(node,path)
                    imp_func_strs[path].append((module,fn_name))
                else:
                    print("No module found "+ast.dump(node))
            elif isinstance(node,ast.Import):
                module = getImportModule(node,path)
                imp_mods[path].append(module)
    return fdefs,imp_func_strs,imp_mods

def matchImpFuncStrs(fdefs,imp_func_strs):
    imp_funcs=dict()
    imp_class_strs=dict()
    for source in imp_func_strs:
        if imp_func_strs[source]==[]:
            break
        imp_funcs[source]=[]
        imp_class_strs[source]=[]
        for (mod,func) in imp_func_strs[source]:
            if mod not in fdefs:
                print(mod+" is not part of the project.")
                break
            if func=='*':
                all_fns = [x for x in fdefs[mod] if x.name!='body']
                imp_funcs[source] += all_fns
            else:
                fn_node = [x for x in fdefs[mod] if x.name==func]
                if fn_node==[]:
                    imp_class_strs[source].append((mod,func))
                else:
                    imp_funcs[source] += fn_node
    return imp_funcs,imp_class_strs
    
def matchImpClassStrs(fdefs,imp_class_strs):
    imp_methods=dict()
    for source in imp_class_strs:
        if imp_class_strs[source]==[]:
            break
        imp_methods[source]=[]
        for (mod,clss) in imp_class_strs[source]:
            if mod not in fdefs:
                print(mod+" is not part of the project.")
                break
            print(mod)
            print(source)
            valid = lambda x: hasattr(x,"pclass") and hasattr(x.pclass,"name")
            classes = [x.pclass.name for x in fdefs[mod] if valid(x)]
            matches = [x for x in fdefs[mod] if x.pclass==clss]
            print(classes)
            print(len(matches))
    return imp_methods
        

def secondPass(ASTs,fdefs,imp_funcs,imp_mods):
    nfound=0
    calls=[]
    for (root,path) in ASTs:
        for (node,stack) in traversal(root):
            if isinstance(node, ast.Call):
                node.source = getSourceFnDef(stack,fdefs,path)
                node.target = getTargetFnDef(node,path,fdefs,imp_funcs,imp_mods)
                if node.target: 
                    nfound+=1
                calls.append(node)
    print(str(nfound)+" call matches were made")
    return calls

def convert(ASTs,project_path):
    copy_ASTs = copy.deepcopy(ASTs)
    print("Making first pass..")
    fdefs,imp_func_strs,imp_mods = firstPass(ASTs)
    #printFnDefs(fdefs)
    imp_funcs,imp_class_strs=matchImpFuncStrs(fdefs,imp_func_strs)
    imp_methods=matchImpClassStrs(fdefs,imp_class_strs)
    #printImpClassStrs(imp_class_strs)
    #printImpFuncs(imp_funcs)
    print("Making second pass..")
    calls = secondPass(copy_ASTs,fdefs,imp_funcs,imp_mods)
    print(str(len(calls))+" total calls")








