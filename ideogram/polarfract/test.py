import polarfract

nodes = [1,2,3,4,5,6]
edges = [(1,2),(1,3),(1,4),(2,4),(1,5),(5,6)]

nodes,edges=polarfract.read(nodes,edges)
print([x.children for x in nodes.values()])
polarfract.positions(nodes,edges)
#polarfract.display