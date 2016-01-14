from glyphs import *
from random import randint


def test_csv_writers():
    n = 15 # number of test functions to create
    fns = [fn(i,str(i)+"_name") for i in range(n)]
    for i in range(n):
        fns[i].setWeight(randint(1,100))
    for i in range(n):
        for j in range(n):
            if randint(0,3) > 1:
                fns[i].addCall(fns[j])
    writeMatrix(fns)
    writeWeights(fns)
    return fns