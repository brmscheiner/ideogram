import pkgutil
import sys

def getModulePath(project_path,module_name):
    '''Searches for module_name in searchpath and None or the filepath.'''
    sys.path.append(project_path)
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

def getImportFromModule(node):
    return None

def getImportFromFn(node):
    return None

def getImportModule(node,project_path):
    print(project_path)
    try:
        for x in node.names:
            module_name = x.asname if x.asname else x.name
            module_path = getModulePath(project_path,module_name)
            "we good dawg"
            return module_path
    except SyntaxError:
        "we not good dawg"
        return None
                
