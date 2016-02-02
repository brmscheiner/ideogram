import reader
import converter
import writer

class DefInfo: pass
class CallInfo: pass

def getGraphData(path):
	ASTs     = reader.read(path)
	nodeInfo = converter.convert(ASTs)
	writer.write(nodeInfo)


if __name__=="__main__":
	project_directory = "test"
	getGraphData(project_directory)