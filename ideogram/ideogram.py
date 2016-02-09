import reader
import converter
import os
#import writer

def genGraphData(project_path):
    ASTs     = reader.read(project_path)
    nodeInfo = converter.convert(ASTs,project_path)
    #writer.write(nodeInfo)

if __name__=="__main__":
    project_path = os.path.join('test','package','bpl-compiler-master','bpl')
    genGraphData(project_path)