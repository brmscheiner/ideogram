
class test:
	def __init__(self):
		self.exists = True
	def isHere(self):
		if self.exists:
			return True
		return False

		
a = test()
print(a.isHere())