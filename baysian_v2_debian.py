from bayes_opt import BayesianOptimization
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
pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
#pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

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
x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21]

#----------------------------------------------------------------------
n_gene = 22 # number of parameters, number of individual +1
min_ind = numpy.ones(n_gene) * -1.0
max_ind = numpy.ones(n_gene) *  1.0
#for i in range(n_gene): 
  #min_ind[i] = b1[i][0]
  #max_ind[i] = b1[i][1]
  #min_ind[i] = float(x[i]) - float(x[i])*0.1
  #max_ind[i] = float(x[i]) + float(x[i])*0.1
  #print "srarch area: "+min_ind[i]+"|"+max_ind[i]
min_ind[0] = float(x0) - float(x0)*0.1
max_ind[0] = float(x0) + float(x0)*0.1
min_ind[1] = float(x1) - float(x1)*0.1
max_ind[1] = float(x1) + float(x1)*0.1
min_ind[2] = float(x2) - float(x2)*0.1
max_ind[2] = float(x2) + float(x2)*0.1
min_ind[3] = float(x3) - float(x3)*0.1
max_ind[3] = float(x3) + float(x3)*0.1
min_ind[4] = float(x4) - float(x4)*0.1
max_ind[4] = float(x4) + float(x4)*0.1
min_ind[5] = float(x5) - float(x5)*0.1
max_ind[5] = float(x5) + float(x5)*0.1
min_ind[6] = float(x6) - float(x6)*0.1
max_ind[6] = float(x6) + float(x6)*0.1
min_ind[7] = float(x7) - float(x7)*0.1
max_ind[7] = float(x7) + float(x7)*0.1
min_ind[8] = float(x8) - float(x8)*0.1
max_ind[8] = float(x8) + float(x8)*0.1
min_ind[9] = float(x9) - float(x9)*0.1
max_ind[9] = float(x9) + float(x9)*0.1
min_ind[10] = float(x10) - float(x10)*0.1
max_ind[10] = float(x10) + float(x10)*0.1
min_ind[11] = float(x11) - float(x11)*0.1
max_ind[11] = float(x11) + float(x11)*0.1
min_ind[12] = float(x12) - float(x12)*0.1
max_ind[12] = float(x12) + float(x12)*0.1
min_ind[13] = float(x13) - float(x13)*0.1
max_ind[13] = float(x13) + float(x13)*0.1
min_ind[14] = float(x14) - float(x14)*0.1
max_ind[14] = float(x14) + float(x14)*0.1
min_ind[15] = float(x15) - float(x15)*0.1
max_ind[15] = float(x15) + float(x15)*0.1
min_ind[16] = float(x16) - float(x16)*0.1
max_ind[16] = float(x16) + float(x16)*0.1
min_ind[17] = float(x17) - float(x17)*0.1
max_ind[17] = float(x17) + float(x17)*0.1
min_ind[18] = float(x18) - float(x18)*0.1
max_ind[18] = float(x18) + float(x18)*0.1
min_ind[19] = float(x19) - float(x19)*0.1
max_ind[19] = float(x19) + float(x19)*0.1
min_ind[20] = float(x20) - float(x20)*0.1
max_ind[20] = float(x20) + float(x20)*0.1
min_ind[21] = float(x21) - float(x21)*0.1
max_ind[21] = float(x21) + float(x21)*0.1
#----------------------------------------------------------------------

pbounds = {
   'x0': (float(min_ind[0]),float(max_ind[0])),
   'x1': (float(min_ind[1]),float(max_ind[1])),
   'x2': (float(min_ind[2]),float(max_ind[2])),
   'x3': (float(min_ind[3]),float(max_ind[3])),
   'x4': (float(min_ind[4]),float(max_ind[4])),
   'x5': (float(min_ind[5]),float(max_ind[5])),
   'x6': (float(min_ind[6]),float(max_ind[6])),
   'x7': (float(min_ind[7]),float(max_ind[7])),
   'x8': (float(min_ind[8]),float(max_ind[8])),
   'x9': (float(min_ind[9]),float(max_ind[9])),
  'x10': (float(min_ind[10]),float(max_ind[10])),
  'x11': (float(min_ind[11]),float(max_ind[11])),
  'x12': (float(min_ind[12]),float(max_ind[12])),
  'x13': (float(min_ind[13]),float(max_ind[13])),
  'x14': (float(min_ind[14]),float(max_ind[14])),
  'x15': (float(min_ind[15]),float(max_ind[15])),
  'x16': (float(min_ind[16]),float(max_ind[16])),
  'x17': (float(min_ind[17]),float(max_ind[17])),
  'x18': (float(min_ind[18]),float(max_ind[18])),
  'x19': (float(min_ind[19]),float(max_ind[19])),
  'x20': (float(min_ind[20]),float(max_ind[20])),
  'x21': (float(min_ind[21]),float(max_ind[21]))}# boundary
print "-----"
print "boundary of parameters: ",pbounds
print "-----"

count = 0
#----------------------------------------------------------------------
def descripter(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21):
  
  print "------------------------"
  global count
  count += 1
  #print count

  fi = open(file_tmp,'r')
  text = fi.read().replace('re',str(x0))
  text = text.replace('fe',str(x1))
  text = text.replace('rhoe1',str(x2))
  text = text.replace('rhoe2',str(x3))
  text = text.replace('alpha',str(x4))
  text = text.replace('beta',str(x5))
  text = text.replace('Ap',str(x6))
  text = text.replace('Bp',str(x7))
  text = text.replace('kappa',str(x8))
  text = text.replace('lambda',str(x9))
  text = text.replace('Fn0',str(x10))
  text = text.replace('Fn1',str(x11))
  text = text.replace('Fn2',str(x12))
  text = text.replace('Fn3',str(x13))
  text = text.replace('F0',str(x14))
  text = text.replace('F1',str(x15))
  text = text.replace('F2',str(x16))
  text = text.replace('F3',str(x17))
  text = text.replace('eta',str(x18))
  text = text.replace('Fep',str(x19))
  text = text.replace('F4',str(x20))
  text = text.replace('rhol',str(x21))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./Zhou04_EAM_3 < EAM.input")
  if count > 2000 or count % int(abs(200-count/10)+1) == 1: 
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
    #
    commands.getoutput("./pwscf2force > config")
  else:
    commands.getoutput(lammps_adress+" < in.lmp_fix")

  # 1 bar = 0.0001 GPa
  # stress = pressure
  pxxl = commands.getoutput("awk '{if($1==\"pxxl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pyyl = commands.getoutput("awk '{if($1==\"pyyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pzzl = commands.getoutput("awk '{if($1==\"pzzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pxyl = commands.getoutput("awk '{if($1==\"pxyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pxzl = commands.getoutput("awk '{if($1==\"pxzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pyzl = commands.getoutput("awk '{if($1==\"pyzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
  pxxp = commands.getoutput("awk '{if($1==\"#S\"){print $2}}' config")
  pyyp = commands.getoutput("awk '{if($1==\"#S\"){print $3}}' config")
  pzzp = commands.getoutput("awk '{if($1==\"#S\"){print $4}}' config")
  pxyp = commands.getoutput("awk '{if($1==\"#S\"){print $5}}' config")
  pxzp = commands.getoutput("awk '{if($1==\"#S\"){print $6}}' config")
  pyzp = commands.getoutput("awk '{if($1==\"#S\"){print $7}}' config")
  diffpxx = (float(pxxl) - float(pxxp))/(float(pxxp)+0.00000010)*100.0/6.0
  diffpyy = (float(pyyl) - float(pyyp))/(float(pyyp)+0.00000010)*100.0/6.0
  diffpzz = (float(pzzl) - float(pzzp))/(float(pzzp)+0.00000010)*100.0/6.0
  diffpxy = (float(pxyl) - float(pxyp))/(float(pxyp)+0.00000010)*100.0/6.0
  diffpxz = (float(pxzl) - float(pxzp))/(float(pxzp)+0.00000010)*100.0/6.0
  diffpyz = (float(pyzl) - float(pyzp))/(float(pyzp)+0.00000010)*100.0/6.0
  diffp = abs(diffpxx) + abs(diffpyy) + abs(diffpzz) + abs(diffpxy) + abs(diffpxz) + abs(diffpyz)
  print "lammps: "+str(pxxl)+", "+str(pyyl)+", "+str(pzzl)+", "+str(pxyl)+", "+str(pxzl)+", "+str(pyzl)+" [eV/A^3]"
  print "pwscf:  "+str(pxxp)+", "+str(pyyp)+", "+str(pzzp)+", "+str(pxyp)+", "+str(pxzp)+", "+str(pyzp)+" [eV/A^3]"
  print "P diff (%): "+str(diffp)
  print "---------------"

  lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%20.10f\",$4}'"
  y_str[0] = commands.getoutput(lammps_get_data)

  pwscf_get_data = "grep \"!    total energy   \" pw.out | tail -1 | awk '{printf \"%20.10f\",$5*13.6058}'"
  target[0] = commands.getoutput(pwscf_get_data)


  potential_get_data = "grep "+str(satom)+" ./potentials/energy_data_for_isolated_atom_reference | head -1 | awk '{printf \"%20.10f\",$2}'"
  target[1] = commands.getoutput(potential_get_data)

  #natom_get_data = "grep \"number of atoms/cell\" pw.out | awk '{printf \"%20.10f\",$5}'"
  #target[2] = commands.getoutput(natom_get_data) 

  print "lammps: ", y_str[0]

  #pwe = float(target[0]) - float(target[1])*float(target[2])
  pwe = float(target[0]) - float(target[1])*float(natom)
  print "PWscf:  ", pwe

  diffe = float(pwe) - float(y_str[0])
  print "diff: ", diffe
  #diffea = float(diffe)/float(target[2])
  diffea = float(diffe)/float(natom)
  print "diff/atom: ", diffea
  commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")
  print "F boundary, diff: "+str(diffb)
  diffb  = commands.getoutput("cat diff.dat")

  print "---------------"
  
  y = 0.001/(float(diffea)**2 + 1000*float(diffb)**2 + 0.0000002*abs(diffp)**2)

  print "Evaluate: ", y
  print "------------------------"

  return y
#----------------------------------------------------------------------
optimizer = BayesianOptimization(f=descripter, pbounds=pbounds)
optimizer.maximize(init_points=1, n_iter=2000, acq="ucb")
#acq = ucb, ei, poi, (default: ubc)

