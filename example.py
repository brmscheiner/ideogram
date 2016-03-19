import ideogram.ideogram as ideogram
import sys 

if __name__=="__main__":
    netwk = ideogram.Chart(outdir='output-network',
                           mode='network',
                           title=('Django','Times New Roman',16,(0,0,0)),
                           colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                           bgcolor=(0,0,0)
                           )
    moire = ideogram.Chart(outdir='output-moire',
                           mode='network',
                           colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                           bgcolor=(0,0,0)
                           )
    ideogram.generate('ideogram',[netwk,moire])
    