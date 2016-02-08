import reader
import converter
import os
#import writer

def genGraphData(path):
    ASTs     = reader.read(path)
    nodeInfo = converter.convert(ASTs)
    #writer.write(nodeInfo)

if __name__=="__main__":
    project_directory = os.path.join('test','package')
    genGraphData(project_directory)