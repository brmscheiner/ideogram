import json
from ideogram import Fn

def writeGraph(functions,outfile="d3js\\outGraph.json"):
    data = dict()
    nodelist = []
    for fn in functions:
        node = dict()
        node["id"]   = fn.sid
        node["file"] = fn.sfilepath
        nodelist.append(node)
    data["nodes"] = nodelist
    linklist = []
    for fn in functions:
        if len(fn.calls) > 0:
            for key in fn.calls:
                link = dict()
                link["source"] = int(fn.sid[1:])
                link["target"] = int(key.sid[1:])
                link["value"]  = fn.calls[key]
                linklist.append(link)
    data["links"] = linklist
    with open(outfile, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def writeHierarchy(functions,outfile="d3js\\outHierarchy.json"):
    
    return

    
    
    
    
    
    
    
    