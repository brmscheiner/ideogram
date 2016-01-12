#from glyphs_analysis import *
import os.path 
import sys
import profile
import pstats
import inspect

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
            
def getPstats(filename,function_name="main"):
    filename = filename[:len(filename)-3]
    exec("import "+filename)    
    module = eval(filename)
    fns = inspect.getmembers(module,inspect.isfunction)
    
    for fn in fns:
        print(fn)
        
    for i in range(len(fns)):
        if fns[i][0] == function_name:
            p = profile.Profile()
            p.runctx(filename+"."+fns[i][0]+"()",globals(),locals())
            s = pstats.Stats(p)
            s.sort_stats("name").strip_dirs().print_callees()
            return s
    return False
    

if __name__== '__main__':
    #filename = getFilename()
    filename = "mandelbrot.py"
    s = getPstats(filename)
    s.print_callers(filename+":")
#    for each in s.stats:
#        print(each)
