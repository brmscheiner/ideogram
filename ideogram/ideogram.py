import ideogram.reader as reader
import ideogram.converter as converter
import ideogram.writer as writer
import os, sys, shutil, requests, urllib.request, zipfile, pystache

class Chart:
    def __init__(self, outdir, mode, title='', font_family='sans-serif', font_size='16px', title_color=(255,255,255), colorscheme=[(0,0,0)], bgcolor=(0,0,0)):
        self.outdir = os.path.abspath(outdir)
        self.mode = mode
        self.title = title
        self.font_family = font_family
        self.font_size = font_size
        self.title_color = title_color
        self.colorscheme = colorscheme
        self.bgcolor = bgcolor 
        self.makeDir()

    def makeDir(self):
        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)

    def build(self,fdefs,calls):
        nout = False
        hout = False
        htmlpath = os.path.abspath(os.path.join(self.outdir, "index.html"))
        d3path = os.path.join("ideogram","templates", "d3.js")
        shutil.copyfile(d3path, os.path.abspath(os.path.join(self.outdir, "d3.js")))
        if os.path.isfile(os.path.join(self.outdir, "nout.json")):
            nout = True
        if os.path.isfile(os.path.join(self.outdir, "hout.json")):
            hout = True
        if self.mode=='network':
            templatepath=os.path.join("ideogram","templates", "force_layout.mustache")
            self.makeHTML(templatepath,htmlpath)
            if not nout:
                csvpath = os.path.join(self.outdir, "nout.json")
                writer.jsonGraph(fdefs,calls,csvpath)
        if self.mode=='moire':
            templatepath=os.path.join("ideogram","templates", "moire.html")
            shutil.copyfile(templatepath,htmlpath)
            if not hout:
                csvpath = os.path.join(self.outdir, "hout.json")
                writer.jsonHierarchy(fdefs,calls,csvpath)
        if self.mode=='pack':
            templatepath=os.path.join("ideogram","templates", "pack_layout.html")
            shutil.copyfile(templatepath,htmlpath)
            if not hout:
                csvpath = os.path.join(self.outdir, "hout.json")
                writer.jsonHierarchy(fdefs,calls,csvpath)
                
    def makeHTML(self,mustachepath,htmlpath):
        '''Write an html file by applying this chart's attributes to a mustache template. '''
        subs = dict()
        if self.title:
            subs["title"]=self.title
            subs["has_title"]=True
        else:
            subs["has_title"]=False
        subs["size"] = self.font_size
        subs["font"] = self.font_family
        with open(mustachepath,'r') as infile:
            mustache_text = pystache.render(infile.read(), subs)
            with open(htmlpath,'w+') as outfile:
                outfile.write(mustache_text)

def generate(path_or_github,charts):
        if isGithubLink(path_or_github):
            name,path = addProject(path_or_github)
            path = os.path.abspath(path)
        elif os.path.isdir(path_or_github):
            path = os.path.abspath(path_or_github)
            name = os.path.basename(path_or_github)
        else:
            print('Cannot make a generator with input '+path_or_github)
            print('Please provide the path to a project directory or a github link.')
            raise(ValueError)
        ASTs = reader.fetch(path)
        fdefs,calls = converter.convert(ASTs,path)
        for c in charts:
            c.build(fdefs,calls)

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
