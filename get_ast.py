# Note: will there be issues using AST on files written in Python 2?

from glyphs import *
import os.path 
import sys
import ast

def isPythonFile(filename):
    if filename[len(filename)-3:] != ".py":
        return False
    return os.path.isfile(filename)

def getFilename():
    if len(sys.argv) != 2:
        filename = input("Enter filename: ").strip()
        while not isPythonFile(filename):
            print("Sorry, that's not a valid filename.")
            filename = input("Enter filename: ").strip()
    else:
        if isPythonFile( sys.argv[1].strip() ): 
            filename = sys.argv[1].strip()
        else:
            sys.stderr.write(sys.argv[1]+" is not a python file")
            raise SystemExit(1)
    return filename
            
def printTree(tree):
    fns = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            print("Function: "+node.name)
            fns.append(node.name)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in fns:
                    print(node.func.id)
#            if isinstance(node.func, ast.Attribute):
#                print(node.func.attr)
                    
def scrape_functions(node):
    fns = []
    n = 0
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
            fns.append(fn(n,node.name))
            n += 1
    return fns
            
def iterative_scrape_calldata(root,fns):
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
                if "current_fn" not in locals():
                    if node.func.id == 'main':
                        pass
                    else:
                        print("Call detected before function definition!")
                        print("Function called: "+node.func.id)
                else:
                    current_fn.addCall(node.func.id)
    return fns
        
    
def recursive_scrape_calldata(node,fns,current_fn='none'):
    # Deprecated because input files will need indeterminate recursion depth.
    if isinstance(node, ast.FunctionDef):
        for fn in fns:
            if fn.name == node.name:
                current_fn = fn
                break
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            current_fn.addCall(node.func.id)
    for each in ast.iter_child_nodes(node):
        fns = scrape_calldata(node,fns,current_fn)
    return fns 

def getAST(filename):
    f = open(filename)
    root = ast.parse(f.read())
    f.close()
    fns = scrape_functions(root)
    fns = iterative_scrape_calldata(root,fns)

if __name__== '__main__':
    #filename = getFilename()
    filename = "mandelbrot.py"
    s = getAST(filename)
    
    
 
