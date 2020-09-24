#from scipy import optimize
import numpy
import numpy as np
import commands
import sys
#----------------------------------------------------------------------
file_tmp = 'EAM_code.tmp'
file_inp = 'EAM_code'

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")
#----------------------------------------------------------------------

x0 = [ 2.556162,1.554485,21.175871,21.175395,8.12762,4.334731,0.39662,0.548085,0.308782,0.756515,-2.170269,-0.263788,1.088878,-0.817603,-2.19,0.0,0.56183,-2.100595,0.31049,-2.186568,-2.100595,0.85 ]

print "------------------------"
print "initial parameters: ",x0

#----------------------------------------------------------------------
def f(x):
  
  print "------------------------"

  fi = open(file_tmp,'r')
  text = fi.read().replace('re',str(x[0]).replace("[","").replace("]",""))
  text = text.replace('fe',str(x[1]).replace("[","").replace("]",""))
  text = text.replace('rhoe1',str(x[2]).replace("[","").replace("]",""))
  text = text.replace('rhoe2',str(x[3]).replace("[","").replace("]",""))
  text = text.replace('alpha',str(x[4]).replace("[","").replace("]",""))
  text = text.replace('beta',str(x[5]).replace("[","").replace("]",""))
  text = text.replace('Ap',str(x[6]).replace("[","").replace("]",""))
  text = text.replace('Bp',str(x[7]).replace("[","").replace("]",""))
  text = text.replace('kappa',str(x[8]).replace("[","").replace("]",""))
  text = text.replace('lambda',str(x[9]).replace("[","").replace("]",""))
  text = text.replace('Fn0',str(x[10]).replace("[","").replace("]",""))
  text = text.replace('Fn1',str(x[11]).replace("[","").replace("]",""))
  text = text.replace('Fn2',str(x[12]).replace("[","").replace("]",""))
  text = text.replace('Fn3',str(x[13]).replace("[","").replace("]",""))
  text = text.replace('F0',str(x[14]).replace("[","").replace("]",""))
  text = text.replace('F1',str(x[15]).replace("[","").replace("]",""))
  text = text.replace('F2',str(x[16]).replace("[","").replace("]",""))
  text = text.replace('F3',str(x[17]).replace("[","").replace("]",""))
  text = text.replace('eta',str(x[18]).replace("[","").replace("]",""))
  text = text.replace('Fep',str(x[19]).replace("[","").replace("]",""))
  text = text.replace('F4',str(x[20]).replace("[","").replace("]",""))
  text = text.replace('rhol',str(x[21]).replace("[","").replace("]",""))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./Zhou04_EAM_3 < EAM.input")
  
  y = 0.0

  print "made EAM potential"
  print "  "+str(satom)+"_Zhou04.eam.alloy"
  print "------------------------"

  return y
#----------------------------------------------------------------------
res = f(x0)
#res = optimize.minimize(f,x0,method='Nelder-Mead',options={'adaptive':True})
#res = optimize.minimize(f,x0,method='Nelder-Mead')
#res = optimize.minimize(f,x0,method='TNC')
#res = optimize.minimize(f,x0,method='Powell')
#res = optimize.minimize(f,x0,method='BFGS')
