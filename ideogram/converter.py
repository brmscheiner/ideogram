import ast

def show(node):
	ast.dump(node)

def isImport(node):
	pass

def isClassDef(node):
	pass

def isCall(node):
	pass

def isFnDef(node):
	pass

def traversal(root):
	# yield node objects in order described in notes
	# add parent and type attributes to node

def getFileDefs(root):
	fnDefs = []
	for node in traversal(root):
		if node.type = "FnDef":

def getProjectDefs(ASTs):
	fnDefs = []
	for (root,__) in ASTs:
		fnDefs += getFileDefs(root)
	return fnDefs