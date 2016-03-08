import polarfract

rawnodes = [1,2,3,4,5,6]
rawedges = [(1,2),(1,3),(1,4),(2,4),(1,5),(5,6)]

nodes=polarfract.read(rawnodes,rawedges)
print(nodes)
#polarfract.positions(nodes,edges)
#polarfract.display