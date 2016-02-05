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

def traversal(root):
	'''For each subtree, evaluate the leaf nodes. If leaf nodes have already been 
	evaluated, their parent nodes become the new leaf nodes.'''
	stack = [root]
	while len(stack) > 0:
		node = stack.pop()
		if hasattr(node,'children'):
			if node.children == set():
				try:
					stack[-1].children.remove(node)
				except:
					pass
				yield (node,stack)
			else:
				childnode = node.children.pop()
				stack += [node,childnode]
		else: 
			children = [x for x in ast.iter_child_nodes(node)]
			node.children = set(children)
			stack.append(node)

def firstPass(ASTs):
	fdefs=[]
	for (root,path) in ASTs:
		for (node,stack) in traversal(root):
			if isinstance(node,ast.FunctionDef):
				#node.name = getFnDefName(node)
				node.weight = calcWeight(node)
				node.path   = path
				node.pclass = getCurrentClass(stack)
				fdefs.append(node)

def secondPass(ASTs):
	calls=[]
	for (root,path) in ASTs:
		for (node,stack) in traversal(root):
			if isinstance(node, ast.Call):
				node.source = getCurrentFnDef(stack)
				calls.append(node)


def convert(ASTs):
	#print(ASTs)
	firstPass(ASTs)












