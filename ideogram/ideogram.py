from . import reader
from . import converter
from . import writer
from . import options_list
import os, sys, shutil, requests, random, zipfile, pystache

class Ideogram:
    def __init__(self, outdir, mode, title='', font_family='sans-serif', font_size='16px', title_color='rgb(0,0,0)', colorscheme='Spectral', bgcolor='rgb(255,255,255)'):
        self.outdir = os.path.abspath(outdir)
        self.mode = mode
        self.title = title
        self.font_family = font_family
        self.font_size = font_size
        if title_color.lower() == 'random':
            self.title_color = random.choice(options_list.colors)
        else:
            self.title_color = title_color
        if colorscheme.lower() == 'random':
            self.colorscheme = random.choice(options_list.schemes)
        else:
            self.colorscheme = colorscheme
        if bgcolor.lower() == 'random':
            self.bgcolor = random.choice(options_list.colors)
        else:
            self.bgcolor = bgcolor 
            
        self.cleanDir()
        self.makeDir()

    def cleanDir(self):
        ''' Remove existing json datafiles in the target directory. '''
        if os.path.isdir(self.outdir):
            baddies = ['tout.json','nout.json','hout.json']
            for file in baddies:
                filepath = os.path.join(self.outdir,file)
                if os.path.isfile(filepath):
                    os.remove(filepath)
        
    def makeDir(self):
        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)

    def build(self,fdefs,calls):
        nout = False
        hout = False
        tout = False
        if os.path.isfile(os.path.join(self.outdir, "nout.json")):
            nout = True
        if os.path.isfile(os.path.join(self.outdir, "hout.json")):
            hout = True
        if os.path.isfile(os.path.join(self.outdir, "tout.json")):
            tout = True
        
        BASE_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
        htmlpath = os.path.abspath(os.path.join(self.outdir, "index.html"))
        d3path = os.path.join(BASE_SCRIPT_PATH,"templates", "d3.js")
        brewpath = os.path.join(BASE_SCRIPT_PATH,"templates", "colorbrewer.js")
        shutil.copyfile(d3path, os.path.abspath(os.path.join(self.outdir, "d3.js")))
        shutil.copyfile(brewpath, os.path.abspath(os.path.join(self.outdir, "colorbrewer.js")))
        if self.mode=='network':
            templatepath=os.path.join(BASE_SCRIPT_PATH,"templates", "force_layout.mustache")
            self.makeHTML(templatepath,htmlpath)
            if not nout:
                csvpath = os.path.join(self.outdir, "nout.json")
                writer.jsonGraph(fdefs,calls,csvpath)
        if self.mode=='moire':
            templatepath=os.path.join(BASE_SCRIPT_PATH,"templates", "moire_layout.mustache")
            self.makeHTML(templatepath,htmlpath)
            if not hout:
                csvpath = os.path.join(self.outdir, "hout.json")
                writer.jsonHierarchy(fdefs,calls,csvpath)
        if self.mode=='pack':
            templatepath=os.path.join(BASE_SCRIPT_PATH,"templates", "pack_layout.mustache")
            self.makeHTML(templatepath,htmlpath)
            if not hout:
                csvpath = os.path.join(self.outdir, "hout.json")
                writer.jsonHierarchy(fdefs,calls,csvpath)
        if self.mode=='depth':
            templatepath=os.path.join(BASE_SCRIPT_PATH,"templates", "depth_layout.mustache")
            self.makeHTML(templatepath,htmlpath)
            if not tout:
                csvpath = os.path.join(self.outdir, "tout.json")
                writer.jsonTree(fdefs,calls,csvpath)
                
    def makeHTML(self,mustachepath,htmlpath):
        '''Write an html file by applying this ideogram's attributes to a mustache template. '''
        subs = dict()
        if self.title:
            subs["title"]=self.title
            subs["has_title"]=True
        else:
            subs["has_title"]=False
        subs["font_size"] = self.font_size
        subs["font_family"] = self.font_family
        subs["colorscheme"] = self.colorscheme
        subs["title_color"] = self.title_color
        subs["bgcolor"] = self.bgcolor
        with open(mustachepath,'r') as infile:
            mustache_text = pystache.render(infile.read(), subs)
            with open(htmlpath,'w+') as outfile:
                outfile.write(mustache_text)

def generate(path_or_github,*args):
        if isGithubLink(path_or_github):
            name,path = addProject(path_or_github)
            path = os.path.abspath(path)
        elif os.path.isdir(path_or_github):
            path = os.path.abspath(path_or_github)
            name = os.path.basename(path_or_github)
        else:
            print('Cannot make a generator with input '+path_or_github)
            print('Please provide the path to a project directory or a github link.')
            print('Argument supplied: '+path_or_github)
            raise(ValueError)
        ASTs = reader.fetch(path)
        fdefs,calls = converter.convert(ASTs,path)
        for c in args:
            c.build(fdefs,calls)
        if isGithubLink(path_or_github):
            shutil.rmtree('temp_data')

def addProject(gh_link):
    ''' Adds a github project to the data folder, unzips it, and deletes the zip file.
    Returns the project name and the path to the project folder. '''
    name = os.path.basename(gh_link)
    zipurl = gh_link+"/archive/master.zip"
    outzip = os.path.join('temp_data',name+'.zip')
    if not os.path.exists('temp_data'):
        os.makedirs('temp_data')
    downloadFile(zipurl,outzip)
    zip = zipfile.ZipFile(outzip,mode='r')
    outpath = os.path.join('temp_data',name)
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

def downloadFile(url,outfile=None): 
    ''' Copied from  http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py '''
    if not outfile:
        outfile = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(outfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)
    return outfile