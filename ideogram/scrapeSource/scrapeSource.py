import reader, converter, writer # 
import os, sys
import urllib.request,zipfile,shutil # downloading, unzipping and cleaning gh projects
# shutil.rmtree(directory) will delete a directory and all of its contents

def getDeepestDirectory(path):
    # ''' Returns the substring following the last backslash in a string. '''
    return path.split(sep='/')[-1]

def addProject(gh_link):
    ''' Adds a github project to the data folder, unzips it, and deletes the zip file.
    Returns the project name and the path to the project folder. '''
    name = getDeepestDirectory(gh_link)
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
    return True
    
def isGithubLink(string):
    return False
    
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
        print(self.name)
        print(self.path)

def genGraphData(project_path):
    ASTs         = reader.fetch(project_path)
    fdefs,calls  = converter.convert(ASTs,project_path)
    project_name = getDeepestDirectory(project_path)
    writer.jsonHierarchy(fdefs,calls,outfile=project_name+"_hout.json")
    writer.jsonGraph(    fdefs,calls,outfile=project_name+"_nout.json")

if __name__=="__main__":
    path_or_github = sys.argv[1]
    g = Generator(path_or_github)