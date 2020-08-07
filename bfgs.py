from scipy import optimize
import numpy
import numpy as np
import commands
import sys
#----------------------------------------------------------------------
file_tmp = 'EAM_code.tmp'
file_inp = 'EAM_code'

lammps_adress = "lmp"
cif2cell_adress = "cif2cell"

commands.getoutput("setenv OMP_NUM_THREADS 1")
num_core = commands.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")
#pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")
print satom

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
commands.getoutput("chmod +x pwscf2force")
commands.getoutput("chmod +x setinp")
commands.getoutput("./setinp")
commands.getoutput("mkdir cfg")
commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

temp_K = commands.getoutput("awk '{if($2==\"temp\"){print $4}}' in.lmp")
print "Lammps MD: "+temp_K+" K"

target = [0,0,0] # dummy data
y_str = [0] # dummy data
natom = commands.getoutput("awk '{if($2==\"atoms\"){print $1}}' data.in")
#----------------------------------------------------------------------
print "read parameters from EAM_code.init"
nline = commands.getoutput("grep -n "+str(satom)+" EAM_code.init | sed -e \"s/:.*//g\"")
print "read line: "+nline
check_satom = commands.getoutput("awk '{if(NR=="+str(nline)+"+0){print $1}}' EAM_code.init | head -1")
print "fit element: "+check_satom
# fitting parameters
x0  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+1){print $1}}' EAM_code.init | head -1"))
x1  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+2){print $1}}' EAM_code.init | head -1"))
x2  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+3){print $1}}' EAM_code.init | head -1"))
x3  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+4){print $1}}' EAM_code.init | head -1"))
x4  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+5){print $1}}' EAM_code.init | head -1"))
x5  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+6){print $1}}' EAM_code.init | head -1"))
x6  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+7){print $1}}' EAM_code.init | head -1"))
x7  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+8){print $1}}' EAM_code.init | head -1"))
x8  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+9){print $1}}' EAM_code.init | head -1"))
x9  = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+10){print $1}}' EAM_code.init | head -1")) 
x10 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+11){print $1}}' EAM_code.init | head -1"))
x11 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+12){print $1}}' EAM_code.init | head -1"))
x12 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+13){print $1}}' EAM_code.init | head -1"))
x13 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+14){print $1}}' EAM_code.init | head -1"))
x14 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+15){print $1}}' EAM_code.init | head -1"))
x15 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+16){print $1}}' EAM_code.init | head -1"))
x16 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+17){print $1}}' EAM_code.init | head -1"))
x17 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+18){print $1}}' EAM_code.init | head -1"))
x18 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+19){print $1}}' EAM_code.init | head -1"))
x19 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+20){print $1}}' EAM_code.init | head -1"))
x20 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+23){print $1}}' EAM_code.init | head -1"))
x21 = float(commands.getoutput("awk '{if(NR=="+str(nline)+"+26){print $1}}' EAM_code.init | head -1"))
print "initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21
x0 = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21]

#----------------------------------------------------------------------
# boundary settings
#n_gene = 22 # number of parameters
#b1 = np.zeros([n_gene,2]) #or np.ones, np.empty
#for i in range(n_gene):
#  b1[i][0] = float(x0[i]) - float(x0[i])*0.1
#  b1[i][1] = float(x0[i]) + float(x0[i])*0.1
#print "srarch area of paramters "
#print b1
#----------------------------------------------------------------------

count = 0
#----------------------------------------------------------------------
def f(x):
  
  print "------------------------"
  global count
  count += 1
  print count

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

  commands.getoutput("./Zhou04_EAM_2 < EAM.input")
  commands.getoutput(lammps_adress+" < in.lmp")
  commands.getoutput("cp ./cfg/run.50.cfg run.50.cfg")
  commands.getoutput("./cfg2vasp/cfg2vasp run.50.cfg")
  commands.getoutput("python ./vasp2cif/vasp2cif.py run.50.vasp")
  commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
  commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
  commands.getoutput("./pwscf2force >> config_potfit")
  commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p lammps  -o data_fix.in")
  commands.getoutput(lammps_adress+" < in.lmp_fix")
  commands.getoutput("mv data.in.restart data.in")

  lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%20.10f\",$4}'"
  y_str[0] = commands.getoutput(lammps_get_data)

  pwscf_get_data = "grep \"!    total energy   \" pw.out | tail -1 | awk '{printf \"%20.10f\",$5*13.6058}'"
  target[0] = commands.getoutput(pwscf_get_data)

  potential_get_data = "grep "+str(satom)+" ./potentials/energy_data_for_isolated_atom_reference | head -1 | awk '{printf \"%20.10f\",$2}'"
  target[1] = commands.getoutput(potential_get_data)

  natom_get_data = "grep \"number of atoms/cell\" pw.out | awk '{printf \"%20.10f\",$5}'"
  target[2] = commands.getoutput(natom_get_data) 

  print "lammps: ", y_str[0]

  pwe = float(target[0]) - float(target[1])*float(target[2])
  print "PWscf:  ", pwe

  diffe = float(pwe) - float(y_str[0])
  print "diff: ", diffe
  diffea = float(diffe)/float(target[2])
  print "diff/atom: ", diffea
  commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")


  rhoin  = float(x[2])*float(x[21])
  rhoout = float(x[2])*1.15
  print "---------------"
  print "F boundary 1, rho: "+str(rhoin)
  print "F boundary 2, rho: "+str(x[2])
  print "F boundary 3, rho: "+str(rhoout)
  commands.getoutput("cp "+satom+"_Zhou04.eam.alloy"+" Xx_Zhou04.eam.alloy")
  commands.getoutput("./plot")
  rhoin1  = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoin)+"){print $2}}' | tail -2 | head -1")
  rhoin2  = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoin)+"){print $2}}' | head -2 | tail -1")
  rhoe1   = commands.getoutput("cat F.plt | awk '{if($1<"+str(x[2])+"){print $2}}' | tail -2 | head -1")
  rhoe2   = commands.getoutput("cat F.plt | awk '{if($1>"+str(x[2])+"){print $2}}' | head -2 | tail -1")
  rhoout1 = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoout)+"){print $2}}' | tail -2 | head -1")
  rhoout2 = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoout)+"){print $2}}' | head -2 | tail -1")
  print "F near boundary 1, F: "+str(rhoin1)+" | "+str(rhoin2)+" | diff "+str(float(rhoin1) - float(rhoin2))
  print "F near boundary 2, F: "+str(rhoe1)+" | "+str(rhoe2)+" | diff "+str(float(rhoe1) - float(rhoe2))
  print "F near boundary 3, F: "+str(rhoout1)+" | "+str(rhoout2)+" | diff "+str(float(rhoout1) - float(rhoout2))
  print "---------------"

  y = abs(diffea)**2 + 1000*abs(float(rhoin1) - float(rhoin2))**2 + 1000*abs(float(rhoe1) - float(rhoe2))**2 + 1000*abs(float(rhoout1) - float(rhoout2))**2

  print "Evaluate: ", y
  #print "Parameters: ", x
  print "Parameters: x0 = "+"[ "+str(x[0])+","+str(x[1])+","+str(x[2])+","+str(x[3])+","+str(x[4])+","+str(x[5])+","+str(x[6])+","+str(x[7])+","+str(x[8])+","+str(x[9])+","+str(x[10])+","+str(x[11])+","+str(x[12])+","+str(x[13])+","+str(x[14])+","+str(x[15])+","+str(x[16])+","+str(x[17])+","+str(x[18])+","+str(x[19])+","+str(x[20])+","+str(x[21])+" ]"
  print "------------------------"

  return y
#----------------------------------------------------------------------
#res = optimize.minimize(f,x0,method='Nelder-Mead')
#res = optimize.minimize(f,x0,method='Powell')
res = optimize.minimize(f,x0,method='BFGS')
