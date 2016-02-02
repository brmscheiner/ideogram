
def read(filepath):
    ASTs=[]
    for (path,dirs,files) in os.walk(filepath):
        python_files = [x for x in files if x.endswith('.py')] 
        for pfile in python_files:
            ast_root = getAST(path,pfile)
            if ast_root: ASTs.append((ast_root,path,pfile))

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