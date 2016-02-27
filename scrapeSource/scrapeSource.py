import reader
import converter
import os
import writer
import sys 

def genGraphData(project_path):
    ASTs        = reader.fetch(project_path)
    fdefs,calls = converter.convert(ASTs,project_path)
    writer.jsonHierarchy(fdefs,calls)
    writer.jsonGraph(fdefs,calls)

if __name__=="__main__":
    project_path = sys.argv[1]
    #project_path = os.path.join(
    #                            'C:\\','Users','scheinerbock','Desktop',
    #                            'ideogram','scrapeSource','test','erp5','product'
    #                            )
    genGraphData(project_path)