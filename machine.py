import ideogram.ideogram as ideogram

if __name__=="__main__":
    projs = ["https://github.com/pybuilder/pybuilder",
                 "https://github.com/platformio/platformio",
                 "https://github.com/pyinstaller/pyinstaller",
                 "https://github.com/mvantellingen/localshop",
                 "https://github.com/pypa/warehouse",
                 "https://github.com/conda/conda",
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
    n=0
    for proj in projs:
        failed = []
        n+=1
        projname = str(n)
        print(projname)
        try:
            netwk = ideogram.Ideogram(outdir=projname+'_network',
                                                       mode='network',
                                                       colorscheme='random',
                                                       bgcolor='random'
                                                       )
            moire = ideogram.Ideogram(outdir=projname+'_moire',
                                                      mode='moire',
                                                      colorscheme='random',
                                                      bgcolor='random'
                                                      )
            pack = ideogram.Ideogram(outdir=projname+'_pack',
                                                     mode='pack',
                                                     colorscheme='random',
                                                     bgcolor='random'
                                                     )
            depth = ideogram.Ideogram(outdir=projname+'_depth',
                                                      mode='depth',
                                                      colorscheme='random',
                                                      bgcolor='random'
                                                      )
            ideogram.generate(proj,netwk,moire,pack,depth)
        except:
            failed.append((proj,projname))
            continue
            
    print(failed)
    print("finished")