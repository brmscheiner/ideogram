import json
import os

def jsPath(path):
    '''Returns a relative path without \, -, and . so that 
    the string will play nicely with javascript.'''
    shortPath=path.replace(
            "C:\\Users\\scheinerbock\\Desktop\\"+
            "ideogram\\scrapeSource\\test\\","")
    noDash = shortPath.replace("-","_dash_")
    jsPath=noDash.replace("\\","_slash_").replace(".","_dot_")
    return jsPath

def jsName(path,name):
    '''Returns a name string without \, -, and . so that 
    the string will play nicely with javascript.'''
    shortPath=path.replace(
            "C:\\Users\\scheinerbock\\Desktop\\"+
            "ideogram\\scrapeSource\\test\\","")
    noDash = shortPath.replace("-","_dash_")
    jsPath=noDash.replace("\\","_slash_").replace(".","_dot_")
    jsName=jsPath+'_'+name
    return jsName
    
def assignID(ids,jsName):
    if jsName in ids:
        return ids[jsName],ids
    else:
        if ids.values():
            new_id      = max(ids.values())+1
            ids[jsName] = new_id
        else:
            new_id      = 1
            ids[jsName] = new_id
        return new_id,ids

def getTaggedNode(fn,ids):
    fn.jsname = jsName(fn.path,fn.name)
    fn_id,ids = assignID(ids,fn.jsname)
    fn.id = fn_id
    node = dict()
    node["id"]     = fn.id
    node["name"]   = fn.jsname
    node["path"]   = jsPath(fn.path)
    node["weight"] = fn.weight
    return node
    
def isInCalls(fn,calls):
    for call in calls:
        if call.source==fn:
            return True
        if call.target==fn:
            return True
    return False
    
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
    ids = dict()
    nodelist = []
    for fnlist in fdefs.values():
        for fn in fnlist:
            if isInCalls(fn,calls):
                tagged_node = getTaggedNode(fn,ids)
                nodelist.append(tagged_node)
            else:
                print("omitted")
    linklist = [] #list of links, NOT a linked list ;D
    for call in calls:
        for link in linklist:
            if call.source.id == link["source"]:
                if call.target.id == link["target"]:
                    link["value"] += 1
                    break
        else:
            link = dict()
            link["source"] = call.source.id
            link["target"] = call.target.id
            link["value"]  = 1
            linklist.append(link)
    
    data["links"] = linklist
    data["nodes"] = nodelist
    with open(outpath, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def jsonHierarchy(fdefs,calls,outfile='out.json'):
    outpath = os.path.join('data',outfile)
    # build later
    return

