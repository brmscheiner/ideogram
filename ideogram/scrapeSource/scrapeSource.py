import reader
import converter
import os
import writer
import sys 

def getName(project_path):
    return project_path.split(sep='/')[-1]

def genGraphData(project_path):
    ASTs         = reader.fetch(project_path)
    fdefs,calls  = converter.convert(ASTs,project_path)
    project_name = getName(project_path)
    writer.jsonHierarchy(fdefs,calls,outfile=project_name+"_hout.json")
    writer.jsonGraph(    fdefs,calls,outfile=project_name+"_nout.json")

if __name__=="__main__":
    project_path = sys.argv[1]
    #project_path = os.path.join(
    #                            'C:\\','Users','scheinerbock','Desktop',
    #                            'ideogram','scrapeSource','test','erp5','product'
    #                            )
    genGraphData(project_path)