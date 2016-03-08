import matplotlib

class Node:
    def __init__(self,name):
        self.name = name
    def setChildren(self,children):
        self.children = children
    def setPos(self,x,y):
        ''' positions will be centered around a root node with coordinates (0,0). '''
        self.x = x 
        self.y = y
    def setTheta(self,t):
        self.theta = t
class Edge:
    def __init__(self,source,target):
        self.source = source
        self.target = target
    
def getRootNode(nodes,edges):
    '''return the node with the most children'''
    root=None
    max=0
    for x in nodes.values():
        n=0
        for e in edges:
            if e.source==x or e.target==x:
                n+=1
        if n>max:
            max=n
            root=x
    return root
    
def getNextNode(nodes,edges,usednodes,parent):
    '''Get next node in a breadth-first traversal of nodes that have not been used yet'''
    for e in edges:
        if e.source==parent:
            if e.target in usednodes:
                x = e.target
                break
        elif e.target==parent:
            if e.source in usednoes:
                x = e.source
                break
    return x    
    
def buildTree(nodes,edges):
    root = getRootNode(nodes,edges)
    parent = root
    usednodes = [parent]
    while len(usednodes)<len(nodes):
        x = getNextNode(nodes,edges,usednodes,parent)
        usednodes.append(x)
        parent = x
    return root 
    
def display(nodes):
    pass
    
    
def scatter_plot(x,y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y,color='blue',edgecolor='none')
    ax.set_aspect(1./ax.get_data_ratio()) # make axes square
    plt.show()
    
def read(rawnodes,rawedges):
    nodes = dict()
    for x in rawnodes:
        nodes[x]=Node(str(x))
    edges = []
    for (p,q) in rawedges:
        edges.append(Edge(nodes[p],nodes[q]))    
    for x in nodes.values():
        if 
    return nodes,edges
        
if __name__=='__main__':
    pass