import json
import os
import random 

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
    jsName=jsPath+'_slash_'+name
    return jsName
    
def assignID(ids,jsName):
    if jsName in ids:
        return ids[jsName],ids
    else:
        if ids.values():
            new_id      = max(ids.values())+1
            ids[jsName] = new_id
        else:
            new_id      = 0
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
    
def getStartNodes(fdefs,calls):
    '''Return a list of nodes in fdefs that have no inbound edges'''
    s=[]
    for source in fdefs:
        for fn in fdefs[source]:
            inboundEdges=False
            for call in calls:
                if call.target==fn:
                    inboundEdges=True
            if not inboundEdges:
                s.append(fn)
    return s
    
def jsonHierarchy(fdefs,calls,outfile='hout.json'):
    outpath = os.path.join('data',outfile)
    s=getStartNodes(fdefs,calls)
    data = dict()
    data["name"]="data"
    data["children"]=[]
    
    n=0
    used=[]
    while s:
        root = dict()
        root["name"]="Category "+str(n)
        root["children"]=[]
        x=random.choice(s)
        s.remove(x)
        line=[x]
        while line:
            current = line.pop()
            used.append(current)
            line=getNewKids(current,calls,used)+line
            newfn=dict()
            newfn["name"]=jsName(current.path,current.name)
            newfn["size"]=current.weight
            root["children"].append(newfn)
        data["children"].append(root)
        n+=1
        
    with open(outpath, 'w+') as f:
        f.write(json.dumps(data, indent=2))
    return
    
def getChildren(current,calls,blacklist=[]):
    ''' Return a list of the children of current that are not in used. '''
    return [c.target for c in calls if c.source==current and c.target not in blacklist]
    
def jsonTree(fdefs,calls,outfile='tout.json'):
    outpath = os.path.join('data',outfile)
    nodes=[]
    for fdeflist in fdefs.values():
        for x in fdeflist:
            nodes.append(jsName(x.path,x.name))
    edges = [[jsName(c.source.path,c.source.name),jsName(c.source.path,c.target.name)] for c in calls]
    root = graphToForest(nodes,edges)
    root = noEmptyNests(root)
    with open(outpath, 'w+') as f:
        f.write(json.dumps(root, indent=2))
    return root

def noEmptyNests(node):
    '''recursively make sure that no dictionaries inside node contain empty children lists '''
    if type(node)==list:
        for i in node:
            noEmptyNests(i)
    if type(node)==dict:
        for i in node.values():
            noEmptyNests(i)
        if node["children"] == []:
            node.pop("children")
            node["size"]=2
    return node

def graphToForest(nodes, edges):
    root_objs = dict()
    root_objs["name"]="data"
    root_objs["children"]=[]
    unused_nodes = nodes

    # Objectize the nodes as a dictionary from the names
    node_objs = []
    for node in unused_nodes:
        node_objs.append({'name':node, 'children':[]})

    while len(unused_nodes):
        root_node = unused_nodes[0]
        max_edges = 0
        # find the root
        for node in unused_nodes:
            edge_count = len(list_connected_nodes(node, edges))

            if max_edges < edge_count:
                max_edges = edge_count
                root_node = node

        # Save the root as the entry point to the tree
        root_obj = find_node_object(node_objs, root_node)

        # Generate the children
        parent_queue = [root_obj]
        unused_nodes.remove(root_node)
        while len(parent_queue):
            parent = parent_queue.pop(0)
            children = list_connected_nodes(parent['name'], edges)
            for child in children:
                if child in unused_nodes:
                    unused_nodes.remove(child)
                    child_obj = find_node_object(node_objs, child)
                    parent_queue.append(child_obj)
                    parent['children'].append(child_obj)

        root_objs["children"].append(root_obj)

    return root_objs

def list_connected_nodes(node, edges):
    output = []
    for edge in edges:
        if (edge[0] == node):
            output.append(edge[1])
        elif (edge[1] == node):
            output.append(edge[0])
    return output

def find_node_object(node_objs, node_name):
    # Find the node by name in the objectized objects
    for node in node_objs:
        if node['name'] == node_name:
            output_node = node
            break
    return output_node

