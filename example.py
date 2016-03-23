import ideogram.ideogram as ideogram
import sys 

# For help choosing colorschemes: https://bl.ocks.org/mbostock/5577023

if __name__=="__main__":
    netwk = ideogram.Ideogram(outdir='chemtrails_network',
                                               mode='network',
                                               title='Hi Sean',
                                               font_family='sans-serif',
                                               font_size='60px',
                                               title_color='random',
                                               colorscheme='random',
                                               bgcolor='random'
                                               )
    moire = ideogram.Ideogram(outdir='chemtrails_moire',
                                              mode='moire',
                                              colorscheme='Purples'
                                              )
    pack = ideogram.Ideogram(outdir='chemtrails_pack',
                                             mode='pack',
                                             colorscheme='Paired',
                                             bgcolor='rgb(0,0,0)'
                                             )
    depth = ideogram.Ideogram(outdir='chemtrails_depth',
                                              mode='depth',
                                              colorscheme='Set3'
                                              )
    ideogram.generate('reference/test/self',netwk,moire,pack,depth)
    