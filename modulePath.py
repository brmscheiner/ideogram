import pkgutil
import sys

def getModulePath(searchpath,module_name):
    # searches for a module in the system path and 
    # returns the path to the .py file
    sys.path.append(searchpath)
    package = pkgutil.get_loader(module_name)
    if package: 
        if package.get_code(module_name):
            filename = package.get_code(module_name).co_filename
            return filename
    else:
        print ("Module "+module_name+" not found.")
        return None
    
    # AHHH I might still be running their code....
    # see pkgutil docs section on iter_importers for more info
    # https://docs.python.org/2/library/pkgutil.html
    
if __name__== "__main__":
    a=getModulePath('test','mandelbrot')
    print(a)
