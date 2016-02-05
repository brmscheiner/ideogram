
def limitChars(x,numChars):
	if len(x)>numChars:
		diff = len(x)-numChars
		x=x[diff:]
	elif len(x)<numChars:
		add = ' '*(numChars-len(x))
		x+=add
	return x

def printFnDefs(fdefs):
	for x in fdefs:
		print(
			limitChars(x.path,30)+'     '+limitChars(x.name,30)
			+limitChars(str(x.weight),10)+limitChars(str(x.pclass),15)
			)