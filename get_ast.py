#from glyphs_analysis import *
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
            
def getAST(filename):
    pass

if __name__== '__main__':
    #filename = getFilename()
    filename = "mandelbrot.py"
    s = getAST(filename)
    
    
 
