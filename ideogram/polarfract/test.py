import polarfract
import matplotlib

def scatter(x,y):
    ''' Display a basic scatterplot of (x,y) using matplotlib. '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y,color='blue',edgecolor='none')
    ax.set_aspect(1./ax.get_data_ratio()) # make axes square
    plt.show()

rawnodes = [1,2,3,4,5,6]
rawedges = [(1,2),(1,3),(1,4),(2,4),(1,5),(5,6)]

circles=polarfract.getCircles(rawnodes,rawedges)
polarfract.display(circles)
#polarfract.positions(nodes,edges)
#polarfract.display