import reader, converter, writer # 
import os, sys
import requests, urllib.request, zipfile, shutil # downloading, unzipping and cleaning gh projects
# shutil.rmtree(directory) will delete a directory and all of its contents

class Generator:
    def __init__(self,path_or_github):
        if isPath(path_or_github):
            self.path = path_or_github
            self.name = getDeepestDirectory(path_or_github)
        elif isGithubLink(path_or_github):
            self.name,self.path = addProject(path_or_github)
        else:
            print('Cannot make a generator with input '+path_or_github)
            print('Please provide the path to a project directory or a github link.')
            raise(ValueError)
        self.ASTs = reader.fetch(self.path)
        self.fdefs, self.calls = converter.convert(self.ASTs,self.path)
        
    def getNetwork(self):
        outfile = os.path.join(data,self.name+"_nout.json")
        writer.jsonGraph(self.fdefs,self.calls,outfile)
        return outfile
        
    def getHierarchy(self):
        outfile = os.path.join(data,self.name+"_hout.json")
        writer.jsonHierarchy(fdefs,calls,outfile)
        return outfile

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
    
def isPath(a):
    if "github.com" in a or not os.path.isdir(a):
        return False
    return True
    
def isGithubLink(a):
    if "github.com" not in a:
        return False
    try:
        r = requests.head(a)
        if r.status_code == 404:
            return False
    except:
        return False
    return True
    
def getDeepestDirectory(path):
    # ''' Returns the substring following the last backslash in a string. '''
    return path.split(sep='/')[-1]
    
if __name__=="__main__":
    path_or_github = sys.argv[1]
    g = Generator(path_or_github)