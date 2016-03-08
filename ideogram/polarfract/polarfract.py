import matplotlib
import math 

class Circle:
    def __init__(self,name):
        self.name = name
        self.children = []
    def addChild(self,child):
        self.children.append(child)
    def setTheta(self,t,mode='radians'):
        if mode=='radians':
            self.t_radians = t
            self.t_degrees = math.degrees(t)
        elif mode=='degrees':
            self.t_radians = math.radians(t)
            self.t_degrees = t
        else:
            raise NameError("Mode must be either degrees or radians.")
    def calcRadius(self,root_radius,c=0.6):
        if theta not in self:
            raise AttributeError("theta must be set before radius can be calculated.")
        tan_t = math.tan(t_radians)
        self.r = c*root_radius*tan_t/(1-tan_t)
    def calcPosition(self,parent_circle):
        ''' Position the circle tangent to the parent circle with the line connecting the centers of the two circles meeting the x axis at angle theta. '''
        if r not in self:
            raise AttributeError("radius must be calculated before position.")
        if theta not in self:
            raise AttributeError("theta must be set before position can be calculated.")
        x_offset = math.cos(t_radians) * (parent_circle.r + self.r)
        y_offset = math.sin(t_radians) * (parent_circle.r + self.r)
        self.x = parent_circle.x + x_offset
        self.y = parent_circle.y + y_offset
    
def getRootNode(nodes):
    '''Return the node with the most children'''
    max = 0
    root = None
    for i in nodes:
        if len(i.children) > max:
            max = len(i.children)
            root = i
    return root
    
def getNextNode(nodes,usednodes,parent):
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
    
    
def scatter(x,y):
    ''' Display a basic scatterplot of (x,y) using matplotlib. '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y,color='blue',edgecolor='none')
    ax.set_aspect(1./ax.get_data_ratio()) # make axes square
    plt.show()
    
def read(rawnodes,rawedges):
    ''' Example input:
    rawnodes = [1,2,3,4,5,6]
    rawedges = [(1,2),(1,3),(1,4),(2,4),(1,5),(5,6)]
    '''
    nodes = []
    for x in rawnodes:
        i = Circle(str(x))
        for (p,q) in rawedges:
            if p==x:
                i.addChild(q)
        nodes.append(i)
    return nodes
        
if __name__=='__main__':
    pass