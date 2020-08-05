#!/usr/bin/env python

#import commands
import matplotlib.pyplot as plt
import numpy as np

#commands.getoutput("./plot")

npArray = np.loadtxt("energy.dat",delimiter=" ")
x = npArray[:,0]
y = npArray[:,1]
last = len(y)
yr = y[last-100:last]

plt.plot(x,y,label="F")

plt.legend()

plt.show()

var = np.var(yr)
#print ("var:", var) #python3
print "var:",var #pthon2

std = np.std(yr)
#print ("std:", std) #python3
print "std:", sdt #python2

avg = np.average(yr)
#print ("avg:",avg) #python3
print "avg:",avg #python2
