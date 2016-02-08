import ast
import converter

def test_traversal():
	x = ast.parse("if i==1: print('okay')")
	for (node,stack) in converter.traversal(x):
		print(node)

if __name__=="__main__":
	test_traversal()