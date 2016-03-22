from . import printer as pr
from . import importAnalysis as ia
import ast, copy

''' known bugs:

    imp_mods[scanner\scanner.py] contains elements even though 
    scanner\scanner.py imports no modules (only from style imports)
    AND
    import bpl.scanner.token in \compiler.py isn't showing up in 
    imp_mods[\compiler.py]
        
    not picking up asname imports 
    '''
    
def convert(ASTs,project_path,verbose=False):
    copy_ASTs = copy.deepcopy(ASTs)
    if verbose:
        print("Making first pass..")
    fdefs,imp_obj_strs,imp_mods,cdefs = firstPass(ASTs,verbose)
    imp_funcs,imp_classes=matchImpObjStrs(fdefs,imp_obj_strs,cdefs)
    if verbose:
        print("Making second pass..")
    calls = secondPass(copy_ASTs,fdefs,cdefs,imp_funcs,imp_mods,imp_classes)
    return fdefs,calls
    
def traversal(root):
    '''Tree traversal function that generates nodes. For each subtree, the 
    deepest node is evaluated first. Then, the next-deepest nodes are 
    evaluated until all the nodes in the subtree are generated.'''
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
            
def firstPass(ASTs,verbose):
    '''Return a dictionary of function definition nodes, a dictionary of  
    imported object names and a dictionary of imported module names. All three 
    dictionaries use source file paths as keys.'''
    fdefs=dict()
    cdefs=dict()
    imp_obj_strs=dict()
    imp_mods=dict()
    for (root,path) in ASTs:
        fdefs[path] = []
        fdefs[path].append(formatBodyNode(root,path))
        imp_obj_strs[path] = []
        imp_mods[path] = []
        cdefs[path] = []
        for (node,stack) in traversal(root):
            if isinstance(node,ast.FunctionDef):
                fdefs[path].append(formatFunctionNode(node,path,stack))
            elif isinstance(node,ast.ImportFrom):
                module = ia.getImportFromModule(node,path,verbose)
                if module:
                    fn_names = ia.getImportFromObjects(node)
                    for fn_name in fn_names:
                        imp_obj_strs[path].append((module,fn_name))
                else:
                    if verbose:
                        print("No module found "+ast.dump(node))
            elif isinstance(node,ast.Import):
                module = ia.getImportModule(node,path,verbose)
                imp_mods[path].append(module)
            elif isinstance(node,ast.ClassDef):
                node.path=path
                cdefs[path].append(node)
    return fdefs,imp_obj_strs,imp_mods,cdefs
            
def secondPass(ASTs,fdefs,cdefs,imp_funcs,imp_mods,imp_classes):
    nfound=0
    calls=[]
    for (root,path) in ASTs:
        for (node,stack) in traversal(root):
            if isinstance(node, ast.Call):
                node.source = getSourceFnDef(stack,fdefs,path)
                node.target = getTargetFnDef(node,path,fdefs,cdefs,
                                             imp_funcs,imp_mods,imp_classes)
                if node.target: 
                    nfound+=1
                if node.source and node.target:
                    calls.append(node)
    return calls

def getCurrentClass(stack):
    for x in stack:
        if isinstance(x, ast.ClassDef):
            return x
    return None

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
    
def getTargetFnDef(node,path,fdefs,cdefs,imp_funcs,imp_mods,imp_classes):
    ''' Return the function node that the input call node targets. 
    
    Note that cases 2b and 2c might make false matches. If two classes are
    imported by the same program and they both have a method with an identical
    name, then class.method() will be associated with the first class in 
    imp_classes.'''
    
    #CASE 1: calling function inside namespace, like foo(x) or randint(x,y)
    if isinstance(node.func,ast.Name):
        # CASE 1A: calling an infile function
        if path in fdefs:
            for x in fdefs[path]:
                if node.func.id == x.name:
                    return x
        # CASE 1B: calling an imported function
        if path in imp_funcs:
            for x in imp_funcs[path]:
                if node.func.id == x.name: 
                    return x
        # CASE 1C: infile object instantiation, i.e. a=Car()
        if path in cdefs:
            for x in cdefs[path]:
                if node.func.id == x.name:
                    classfuncs = [y for y in fdefs[path] if y.pclass==x]
                    initfuncs = [z for z in classfuncs if z.name=='__init__']
                    if initfuncs:
                        return initfuncs[0]
                        
        # CASE 1D: imported object instantiation, from exe import car; a=Car()
        if path in imp_classes:
            for x in imp_classes[path]:
                if node.func.id == x.name:
                    classfuncs = [y for y in fdefs[x.path] if y.pclass==x]
                    initfuncs = [z for z in classfuncs if z.name=='__init__']
                    if initfuncs:
                        return initfuncs[0]
        return None # builtin functions
        
    # CASE 2: calling function outside namespace, like random.randint(x,y)
    elif isinstance(node.func,ast.Attribute):
        try:
            obj    = node.func.value.id
            method = node.func.attr
        except AttributeError:
            return None #weird string thingies
        if obj == 'self':
            return None #setting attrs in class def.
        # CASE 2A: calling imported module.function
        for modpath in imp_mods[path]:
            if not modpath:
                continue
            elif obj+'.py' in modpath:
                if modpath in fdefs:
                    matches = [x for x in fdefs[modpath] if x.name==method]
                    if matches:
                        if len(matches)>1:
                            pass
                            #print("multiple matches found for "+method)
                        return matches[0]
                    
            # CASE 2B: object instantiation with an imported module
            if modpath not in cdefs:
                continue
            for clss in cdefs[modpath]:
                if clss.name==method:
                    classfuncs = [y for y in fdefs[clss.path] if y.pclass==clss]
                    initfuncs = [z for z in classfuncs if z.name=='__init__']
                    if initfuncs:
                        return initfuncs[0]
                    
        # CASE 2C: calling infile class.method 
        if path in cdefs:
            for clss in cdefs[path]:
                for x in fdefs[clss.path]:
                    if x.pclass==clss:
                        return x
                    
        # CASE 2D: calling imported class.method         
        if path in imp_classes:
            for clss in imp_classes[path]:
                for x in fdefs[clss.path]:
                    if x.pclass==clss:
                        if x.name==method:
                            return x
                            
        return None #sys.method type calls, also some random builtins
                    

def matchImpObjStrs(fdefs,imp_obj_strs,cdefs):
    '''returns imp_funcs, a dictionary with filepath keys that contains 
    lists of function definition nodes that were imported using
     from __ import __ style syntax. also returns imp_classes, which 
    is the same for class definition nodes.'''
    imp_funcs=dict()
    imp_classes=dict()
    for source in imp_obj_strs:
        if not imp_obj_strs[source]:
            continue
        imp_funcs[source]=[]
        imp_classes[source]=[]
        for (mod,func) in imp_obj_strs[source]:
            if mod not in fdefs:
                #print(mod+" is not part of the project.")
                continue
            if func=='*':
                all_fns = [x for x in fdefs[mod] if x.name!='body']
                imp_funcs[source] += all_fns
                all_cls = [x for x in cdefs[mod]]
                imp_classes[source] += all_cls
            else:
                fn_node = [x for x in fdefs[mod] if x.name==func]
                cls_node = [x for x in cdefs[mod] if x.name==func]
                #assert len(fn_node) in [1,0]
                #assert len(cls_node) in [1,0]
                if cls_node:
                    imp_classes[source] += cls_node
                if fn_node:
                    imp_funcs[source] += fn_node
                if not fn_node and not cls_node:
                    pass
                    #print(func+' not found in function and class definitions.')
    return imp_funcs,imp_classes




    
    
    
    






