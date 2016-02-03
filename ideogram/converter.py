import ast

def show(node):
	ast.dump(node)

def isImport(node):
	pass

def getCurrentClass(stack):
	for x in stack:
		if isinstance(x, ast.ClassDef):
			return x
	return None

def getCurrentFnDef(stack):
	for x in stack:
		if isinstance(x, ast.FunctionDef):
			return x
	return None # return "body?"

def calcWeight(node):
	'''Calculates the weight of a function definition by 
	recursively counting its child nodes in the AST. Note
	that the tree traversal will become O(n^2) instead of 
	O(n)'''
	stack = [node]
	count = 0
	while len(stack) > 0:
		node = stack.pop()
		children = [x for x in ast.iter_child_nodes(node)]
		count += len(children)
		stack = stack + children
	return count

def cullChildList(stack,node):
	newstack = []
	for x in stack:
		if node in x.children:
			x.children.remove(node)
			newstack.append(x)
	return newstack

def traversal(root,fdefs=True,calls=True):
	stack     = [root]
	processed = []
	while len(stack) > 0:
		node = stack.pop()
		children = [x for x in ast.iter_child_nodes(node)]
		if children: 
			node.children = set(children)
			stack.append(node)
			stack = stack + children
		else:
			stack = cullChildList(stack,node)
			if fdefs and isinstance(x, ast.FunctionDef):
				node.type   = "fdef"
				node.pclass = getCurrentClass(stack)
				yield node
			elif calls and isinstance(node, ast.Call):
				node.type   = "call"
				node.source = getCurrentFnDef(stack)
				yield node

def firstPass(ASTs):
	fdefs=[]
	for (root,path) in ASTs:
		for node in traversal(root,fdefs=True,calls=False):
			node.weight = calcWeight(node)
			node.path = path
			fdefs.append(node)


def convert(ASTs):
	print(ASTs)
	firstPass(ASTs)












