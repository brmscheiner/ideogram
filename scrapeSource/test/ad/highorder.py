import differentiator
import evaluator

class higherorder(self):
	def __init__(self,order):
		self.order=order
	def evaluate(self,fn,x):
		return self.evaluateHelper(fn,x,self.order)
	def evaluateHelper(self,fn,x,i):
		if i==0:
			evaluator = evaluator.evaluator(fn,x)
			return evaluator.evaluate(fn,x)
		if i>=1:
			derivative = differentiator(fn).getDerivative()
			return evaluateHelper(derivative,x,i-1)
		
if __name__ == "__main__":
	obj = higherorder(5)
	dn = obj.evaluate("sin(x)",0)
	print(dn.dump())