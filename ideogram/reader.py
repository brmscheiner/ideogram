import ast
import os
import subprocess

def fetch(project_path):
    ASTs=[]
    for (dirpath,__,files) in os.walk(project_path):
        python_files = [x for x in files if x.endswith('.py')]
        for pfile in python_files:
            path = os.path.join(dirpath,pfile)
            ast_root = getAST(path)
            if ast_root: 
                ASTs.append((ast_root,path))
    return ASTs

def getAST(path):
    try:
        with open(path) as f:
            root = ast.parse(f.read())
    except: # if the program wont compile maybe its written for Python 2.x
        try:
            subprocess.call(["2to3","-w",module.name])
            with open(path) as f:
                root = ast.parse(f.read())
        except:
            print("File "+path+" wont compile! Ignoring...")
            return None
    return root