import reader
import converter
#import writer

def genGraphData(path):
	ASTs     = reader.read(path)
	nodeInfo = converter.convert(ASTs)
	#writer.write(nodeInfo)

if __name__=="__main__":
	project_directory = "/Users/babe/Documents/glyph/test/package"
	genGraphData(project_directory)