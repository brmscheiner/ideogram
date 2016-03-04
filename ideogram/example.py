import ideogram

if __name__=="__main__":
	g = ideogram.generator('ideogram')   # process functions and calls in the ideogram directory 
	n = g.network()                      # generate network data 
	n.write('network.html')              # output a network graph visualization
	h = g.hierarchy()
	h.write('hierarchy.html')