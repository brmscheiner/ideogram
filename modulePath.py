import inspect 
import sys

# look into virtualenv if this causes namespace issues

def getModulePath(path,module_name):
    sys.path.append(path)
    pfile=None
    exec("import "+module_name)
    exec("pfile = inspect.getfile("+module_name+")")
    if pfile.endswith(".pyc"):
        pfile = pfile[:len(pfile)-1]
    return pfile
    
if __name__== "__main__":
    a=getModulePath('test','mandelbrot')
    print(a)
