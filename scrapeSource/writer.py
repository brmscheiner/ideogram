import json
import os

def jsName(path,name):
    '''Returns a relative path with "_"s instead of "\"s
    so that the string will play nicely with javascript.'''
    shortPath=path.replace(
            "C:\\Users\\scheinerbock\\Desktop\\"+
            "ideogram\\scrapeSource\\test\\","")
    noDash = shortPath.replace("-","_dash_")
    jsPath=noDash.replace("\\","_slash_").replace(".","_dot_")
    return jsPath+'_'+name

def jsonGraph(fdefs,calls,outfile='out.json'):
    '''For reference, each node has:
    
    node.name   (string)
    node.source (string)
    node.weight (int)
    node.pclass (class node object) 
    
    Each call contains a node in call.source and call.target
    '''
    outpath = os.path.join('data',outfile)
    data = dict()
    nodelist = []
    for fnlist in fdefs.values():
        for fn in fnlist:
            fn.jsid = jsName(fn.path,fn.name)
            node = dict()
            node["id"]     = fn.jsid
            node["weight"] = fn.weight
            nodelist.append(node)
    data["nodes"] = nodelist
    linklist = [] #list of links, NOT a linked list ;D
    for call in calls:
        for link in linklist:
            print(call.source)
            print(call.source.jsid)
            print(type(link))
            if call.source.jsid == link["source"]:
                if call.target.jsid == link["target"]:
                    link["value"] += 1
                    break
        else:
            link = dict()
            link["source"] = call.source.jsid
            link["target"] = call.target.jsid
            link["value"]  = 1
            linklist.append(link)
    data["links"] = linklist
    with open(outpath, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def jsonHierarchy(fdefs,calls,outfile='out.json'):
    outpath = os.path.join('data',outfile)
    # build later
    return

