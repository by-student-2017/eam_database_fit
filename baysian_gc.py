from bayes_opt import BayesianOptimization
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
pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
#pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
commands.getoutput("chmod +x pwscf2force")
commands.getoutput("cp data.in data.in.origin")
commands.getoutput("mkdir cfg")
commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

temp_K = commands.getoutput("awk '{if($2==\"temp\"){print $4}}' in.lmp")
print "Lammps MD: "+temp_K+" K"

target = [0,0,0] # dummy data
y_str = [0] # dummy data

# fitting parameters
x0 =   2.556162
x1 =   1.554485
x2 =  21.175871
x3 =  21.175871
x4 =   8.127620
x5 =   4.334731
x6 =   0.396620
x7 =   0.548085
x8 =   0.308782
x9 =   0.756515
x10 = -2.170269
x11 = -0.263788
x12 =  1.088878
x13 = -0.817603
x14 = -2.190000
x15 =  0.561830
x16 = -2.100595
x17 =  0.310490
x18 = -2.186568

pbounds = {
   'x0': (2.000000,4.200000),
   'x1': (0.400000,4.200000),
   'x2': (5.700000,44.700000),
   'x3': (5.700000,44.700000),
   'x4': (5.700000,12.000000),
   'x5': (3.000000,6.500000),
   'x6': (0.100000,1.100000),
   'x7': (0.200000,1.700000),
   'x8': (0.100000,0.60),
   'x9': (0.200000,1.20),
  'x10': (-6.100000,-0.700000),
  'x11': (-2.500000,-0.030000),
  'x12': (-0.600000,1.9400000),
  'x13': (-5.300000,-0.550000),
  'x14': (-6.10,-0.70),
  'x15': (0.480000,3.600000),
  'x16': (-3.00000,0.930000),
  'x17': (0.300000,1.740000),
  'x18': (-6.100000,-0.66000)}# boundary

count = 0
#----------------------------------------------------------------------
def descripter(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18):
  
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
  text = text.replace('F2',str(x15))
  text = text.replace('F3',str(x16))
  text = text.replace('eta',str(x17))
  text = text.replace('Fep',str(x18))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./gen_eam < EAM.input")
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


  potential_get_data = "grep "+str(satom)+" ./potentials/energy_data_for_isolated_atom_reference | awk '{printf \"%20.10f\",$2}'"
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

  y = 0.001/abs(diffea)

  print "Evaluate: ", y
  print "------------------------"

  return y
#----------------------------------------------------------------------
optimizer = BayesianOptimization(f=descripter, pbounds=pbounds)
optimizer.maximize(init_points=1, n_iter=2000, acq="ucb")
#acq = ucb, ei, poi, (default: ubc)

