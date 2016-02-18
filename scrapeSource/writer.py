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
            fn.jsname = jsName(fn.path,fn.name)
            fn_id,ids = assignID(ids,fn.jsname)
            fn.id = fn_id
            node = dict()
            node["id"]     = fn.id
            node["name"]   = fn.jsname
            node["weight"] = fn.weight
            nodelist.append(node)
    data["nodes"] = nodelist
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
    with open(outpath, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def jsonHierarchy(fdefs,calls,outfile='out.json'):
    outpath = os.path.join('data',outfile)
    # build later
    return

