
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