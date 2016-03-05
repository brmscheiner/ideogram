import ideogram
import sys 

if __name__=="__main__":
    project_path = sys.argv[1]
    g = ideogram.Generator(project_path) # this could take a while for large projects..
    n = g.getNetworkData() 
    g.writeNetwork('network.html')
    g.getHierarchyData()
    h.write('hierarchy.html')