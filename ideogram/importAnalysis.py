import pkgutil
import sys

def getModulePath(project_path,module_name):
    '''Searches for module_name in searchpath and returns the filepath.
    If no filepath was found, returns None.'''
    sys.path.append(project_path)
    try:
        package = pkgutil.get_loader(module_name)
    except ImportError:
        package = None
    if package: 
        if package.get_code(module_name):
            filename = package.get_code(module_name).co_filename
            return filename
    else:
        print ("Module "+module_name+" not found.")
        return None

def getImportFromModule(node):
    return None

def getImportFromFn(node):
    return None

def getImportModule(node,filepath):
    path = filepath[:filepath.rfind("\\")]
    for x in node.names:
        module_name = x.asname if x.asname else x.name
        module_path = getModulePath(path,module_name)
        return module_path
            
