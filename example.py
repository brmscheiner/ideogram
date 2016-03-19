import ideogram.ideogram as ideogram
import sys 

if __name__=="__main__":
    netwk = ideogram.Chart(outdir='brewery',
                                     mode='network',
                                     title='A well-brewed recipe.',
                                     font_family='sans-serif',
                                     font_size='46px',
                                     title_color=(255,255,255),
                                     colorscheme='Spectral',
                                     bgcolor=(0,0,0)
                                     )
    moire = ideogram.Chart(outdir='output-moire',
                           mode='network',
                           colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                           bgcolor=(0,0,0)
                           )
    ideogram.generate('ideogram',[netwk,moire])
    