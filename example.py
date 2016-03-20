import ideogram.ideogram as ideogram
import sys 

if __name__=="__main__":
    netwk = ideogram.Chart(outdir='brewery',
                                          mode='depth',
                                          title='jackalope',
                                          font_family='sans-serif',
                                          font_size='60px',
                                          title_color='rgb(50,150,150)',
                                          colorscheme='Greys',
                                          bgcolor='rgb(155,45,0)'
                                          )
    moire = ideogram.Chart(outdir='output-moire',
                                          mode='network',
                                          colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                                          bgcolor=(0,0,0)
                                          )
    ideogram.generate('ideogram',[netwk,moire])
    