import json
from ideogram import Fn

def jsonGraph(functions,outfile=['d3js','out.json']):
    outpath = os.path.join(*outfile)
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
    with open(outpath, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def jsonHierarchy(functions,outfile=['d3js','out.json']):
    outpath = os.path.join(*outfile)
    # build later
    return

