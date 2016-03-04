import reader, converter, writer # 
import os, sys
import urllib.request,zipfile,shutil # downloading, unzipping and cleaning gh projects

def getDeepestDirectory(path):
    '''return the deepest directory of a path string.
    For example, "/asdf/cwfe/dascd/basdf" returns "basdf" '''
    i = path.find('/')
    while i!=-1:
        i = path.find('/')
        path=path[i+1:]
    return path

def addProject(gh_link):
    '''adds a github project to the data folder, unzips it and returns 
    the project name and the path to the project folder'''
    name = getDeepestDirectory(gh_link)
    print(name)
    zipurl = gh_link+"/archive/master.zip"
    outzip = os.path.join('data',name+'.zip')
    urllib.request.urlretrieve(zipurl,outzip)
    zip = zipfile.ZipFile(outzip,mode='r')
    outpath = os.path.join('data',name)
    zip.extractall(outpath)
    zip.close()
    os.remove(outzip)
    return name,outpath

def isPath(string):
    return False
    
def isGithubLink(string):
    return True
    
class Generator:
    def __init__(self,path_or_github):
        if isPath(path_or_github):
            self.path = path_or_github
            self.name = getDeepestDirectory(path_or_github)
        elif isGithubLink(path_or_github):
            self.name,self.path = addProject(path_or_github)
        else:
            print('Cannot create a generator with input '+path_or_github)
            print('Please provide the path to a project directory or a github link.')
            raise(ValueError)

def getName(project_path):
    return project_path.split(sep='/')[-1]

def genGraphData(project_path):
    ASTs         = reader.fetch(project_path)
    fdefs,calls  = converter.convert(ASTs,project_path)
    project_name = getName(project_path)
    writer.jsonHierarchy(fdefs,calls,outfile=project_name+"_hout.json")
    writer.jsonGraph(    fdefs,calls,outfile=project_name+"_nout.json")

if __name__=="__main__":
    path_or_github = sys.argv[1]
    g = Generator(path_or_github)