import pkgutil
import sys

def getModulePath(project_path,module_name,verbose):
    '''Searches for module_name in searchpath and returns the filepath.
    If no filepath was found, returns None.'''
    if not module_name:
        return None
    sys.path.append(project_path)
    try:
        package = pkgutil.get_loader(module_name)
    except ImportError:
        if verbose:
            print("Parent module for "+module_name+" not found.")
        return None
    except:
        if verbose:
            print(module_name+" not loaded for bizarre reasons")
    try:
        if package: 
                if package.get_code(module_name):
                    filename = package.get_code(module_name).co_filename
                    return filename
                elif package.find_spec(module_name).has_location==False:
                    return None #built-in module such as itertools
                else:
                    pass #perhaps filename is in package.find_spec(module_name).origin?
                    pass #a good reference is https://www.python.org/dev/peps/pep-0302/
    except ImportError:
        if verbose:
            print("Code object unavailable for "+module_name)
        return None
    except AttributeError:
        if verbose:
            print(module_name+" is an ExtensionFileLoader object")
        return None
    except:
        if verbose:
            print(module_name+" not loaded for bizarre reasons")
        return None
    else:
        if verbose:
            print ("Module "+module_name+" not found.")
        return None

def getImportFromModule(node,filepath,verbose):
    path = filepath[:filepath.rfind("\\")]
    module_name = node.module
    return getModulePath(path,module_name,verbose)

def getImportFromObjects(node):
    '''Returns a list of objects referenced by import from node'''
    somenames = [x.asname for x in node.names if x.asname]
    othernames = [x.name for x in node.names if not x.asname]
    return somenames+othernames

def getImportModule(node,filepath,verbose):
    path = filepath[:filepath.rfind("\\")]
    for x in node.names:
        module_name = x.asname if x.asname else x.name
        module_path = getModulePath(path,module_name,verbose)
        return module_path
            
