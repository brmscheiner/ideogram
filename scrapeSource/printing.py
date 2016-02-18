
def show(node):
    print(ast.dump(node))

def getClassString(node):
    if node:
        return node.name
    return 'None'
    
def getPrettyPath(path,numChars):
    if path.find("type_checker_test.py"):
        pass # strange case!!
    path=limitChars(path,numChars)
    if path.find("\\"):
        return limitChars(path[path.find('\\'):],numChars)
    elif path.find("/"):
        return limitChars(path[path.find('/'):],numChars)
    else:
        return path

def limitChars(x,numChars):
    if len(x)>numChars:
        diff = len(x)-numChars
        x=x[diff:]
    elif len(x)<numChars:
        add = ' '*(numChars-len(x))
        x+=add
    return x

def printFnDefs(fdefs):
    fdeflists = list(fdefs.values())
    fdeflist = [item for sublist in fdeflists for item in sublist]
    print(len(fdeflist))
    for x in fdeflist:
        print(
            getPrettyPath(x.path,30)+'     '
            +limitChars(x.name,30)
            +limitChars(str(x.weight),10)
            +limitChars(getClassString(x.pclass),20)
            )
            
def printImpFuncStrs(imp_func_strs):
    for i in imp_func_strs:
        if imp_func_strs[i]:
            print("Functions imported in "+i)
            for (mod,func) in imp_func_strs[i]:
                if func:
                    print("   "+func+" imported from "+mod)
                else:
                    print("   Nothing imported from "+mod)
        else:
            print("No functions imported in file "+i)
            
def printImpObjs(imp_funcs_or_imp_classes):
    a = imp_funcs_or_imp_classes
    for i in a:
        if a[i]:
            print("Objects imported in "+i)
            print([x.name for x in a[i]])
        else:
            print("No objects imported in file "+i)
    
    
    
    
    