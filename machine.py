import ideogram.ideogram as ideogram
import sys 
import os
import random 

if __name__=="__main__":
    projs = ["https://github.com/pybuilder/pybuilder",
                 "https://github.com/platformio/platformio",
                 "https://github.com/pyinstaller/pyinstaller",
                 "https://github.com/mvantellingen/localshop",
                 "https://github.com/pypa/warehouse",
                 "https://github.com/conda/conda/",
                 "https://github.com/nvie/pip-tools",
                 "https://github.com/dirn/When.py",
                 "https://github.com/shnode/PyTime",
                 "https://github.com/zachwill/moment",
                 "https://github.com/myusuf3/delorean/",
                 "https://github.com/dateutil/dateutil",
                 "https://github.com/KoffeinFlummi/Chronyk",
                 "https://github.com/crsmithdev/arrow",
                 "https://github.com/gorakhargosh/watchdog",
                 "https://github.com/mikeorr/Unipath",
                 "https://github.com/ahupp/python-magic",
                 "https://github.com/jaraco/path.py",
                 "https://github.com/jonathanslenders/ptpython",
                 "https://github.com/bpython/bpython",
                 "https://github.com/lincolnloop/python-qrcode",
                 "https://github.com/ajkumar25/pygram",
                 "https://github.com/hhatto/nude.py",
                 "https://github.com/lepture/mistune",
                 "https://github.com/mstamy2/PyPDF2",
                 "https://github.com/euske/pdfminer",
                 "https://github.com/koenbok/Cactus/",
                 "https://github.com/madisonmay/Tomorrow"]
    for proj in projs:
        failed = []
        try:
            projname = os.path.basename(proj)
            netwk = ideogram.Ideogram(outdir=proj+'_network',
                                                       mode='network',
                                                       title='chemtrails_bot',
                                                       font_family='sans-serif',
                                                       font_size='60px',
                                                       title_color='rgb(50,25,60)',
                                                       colorscheme='random',
                                                       bgcolor='rgb(155,45,0)'
                                                       )
            moire = ideogram.Ideogram(outdir=proj+'_moire',
                                                      mode='moire',
                                                      colorscheme=random.choice(schemes)
                                                      )
            pack = ideogram.Ideogram(outdir=proj+'_pack',
                                                     mode='pack',
                                                     colorscheme=random.choice(schemes),
                                                     bgcolor='rgb(0,0,0)'
                                                     )
            depth = ideogram.Ideogram(outdir=proj+'_depth',
                                                      mode='depth',
                                                      colorscheme=random.choice(schemes)
                                                      )
            ideogram.generate(proj,netwk,moire,pack,depth)
        except:
            failed.append((proj,projname))
    print(failed)
    print("finished")
    