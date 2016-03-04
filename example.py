import ideogram
import sys 

if __name__=="__main__":
    project_path = sys.argv[1]
    g = ideogram.Generator('ideogram')   # process functions and calls in the ideogram directory 
    n = g.Network()                      # generate network data 
    n.write('network.html')              # output a network graph visualization
    h = g.Hierarchy()
    h.write('hierarchy.html')