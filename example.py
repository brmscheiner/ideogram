import ideogram
import sys 

if __name__=="__main__":

    # 1.
    project_path = sys.argv[1]
    g = ideogram.Generator(project_path) # this could take a while for large projects..
    n = g.getNetworkData() 
    g.writeNetwork('network.html')
    g.getHierarchyData()
    h.write('hierarchy.html')
    
    # 2.
    ideogram.generate(path='ideogram',
                      gh_link='https://github.com/brmscheiner/ideogram',
                      mode='network',
                      colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                      bg_color=(0,0,0)
                      )

    # 3.
    netwk = ideogram.chart(mode='network',
                           title=('Django','Times New Roman',16,(0,0,0))
                           colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                           bg_color=(0,0,0)
                           )
    moire = ideogram.chart(mode='network',
                           colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                           bg_color=(0,0,0)
                           )
    ideogram.generate('ideogram',netwk,moire)
    