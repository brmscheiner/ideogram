import reader
import converter
import writer

class DefInfo:
	def __init__(self,path,node,pclass):
		self.path   = path
		self.pclass = pclass # name of class if fn is a method of 
		self.name   = self.getName(node)
	def getName(self,node):
		name = None
		return name

class CallInfo: 
	def __init__(self,path,node):
		self.path = path
		self.name = self.getName(node)
	def getName(self,node):
		name = None
		return name
	def setSource(self,source):
		self.source = source
	def setTarget(self,target):
		self.target = target

def getGraphData(path):
	ASTs     = reader.read(path)
	nodeInfo = converter.convert(ASTs)
	writer.write(nodeInfo)

if __name__=="__main__":
	project_directory = "test"
	getGraphData(project_directory)