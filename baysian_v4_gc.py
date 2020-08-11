from bayes_opt import BayesianOptimization
import numpy
import numpy as np
import commands
import sys
#----------------------------------------------------------------------
file_tmp = 'EAM_code.tmp'
file_inp = 'EAM_code'

cif2cell_adress = "cif2cell"

commands.getoutput("setenv OMP_NUM_THREADS 1")
num_core = commands.getoutput("grep 'core id' /proc/cpuinfo | sort -u | wc -l")
lammps_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root lmp"
pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#lammps_adress = "mpirun -np "+str(num_core)+" lmp"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
#lammps_adress = "mpirun -np 2 lmp"
#pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
commands.getoutput("chmod +x pwscf2force")
commands.getoutput("chmod +x setinp")
commands.getoutput("./setinp")
commands.getoutput("mkdir cfg")
commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

natom = 5000
fxl = numpy.ones(int(natom)+1)
fyl = numpy.ones(int(natom)+1)
fzl = numpy.ones(int(natom)+1)
fxp = numpy.ones(int(natom)+1)
fyp = numpy.ones(int(natom)+1)
fzp = numpy.ones(int(natom)+1)

temp = [77,273,1073,1573]
for t in temp:
  commands.getoutput("cp in.lmp in.lmp_"+str(t)+"K")
  commands.getoutput("sed -i 's/YYYY/"+str(t)+"/' in.lmp_"+str(t)+"K")
  commands.getoutput("cp data.in data.in_"+str(t)+"K")
# if you would set other structures, e.g.,
#commands.getoutput("cp data.in data.in_77K")
#commands.getoutput("cp data.in data.in_273K")
#commands.getoutput("cp ./data/data.in.BCC data.in_1073K")
#commands.getoutput("cp ./data/data.in.HCP data.in_1578K")
#----------------------------------------------------------------------
print "read parameters from EAM_code.init"
nline = commands.getoutput("grep -n "+str(satom)+" EAM_code.init | head -1 | sed -e \"s/:.*//g\"")
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

  tdiffea = 0.0
  tdiffp  = 0.0
  tdifff  = 0.0
  for t in temp:
    print "---------------"
    print "Temperature: "+str(t)+" [K]"
    if count > 3000 or count % int(600*2.718**(-count/600)+1) == 1: 
      commands.getoutput("mv data.in_"+str(t)+"K data.in")
      natom = commands.getoutput("awk '{if($2==\"atoms\"){print $1}}' data.in")
      commands.getoutput(lammps_adress+" < in.lmp_"+str(t)+"K")
      commands.getoutput("cp ./cfg/run.50.cfg run.50.cfg")
      commands.getoutput("./cfg2vasp/cfg2vasp run.50.cfg")
      commands.getoutput("python ./vasp2cif/vasp2cif.py run.50.vasp")
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
      commands.getoutput(pwscf_adress+" < pw.scf.in")
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.18 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
      commands.getoutput(pwscf_adress+" < pw.scf.in > pw.out")
      commands.getoutput("./pwscf2force >> config_potfit_"+str(satom))
      commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p lammps -o data_fix.in_"+str(t)+"K")
      commands.getoutput("cp data_fix.in_"+str(t)+"K data_fix.in")
      commands.getoutput(lammps_adress+" < in.lmp_fix")
      commands.getoutput("mv data.in.restart data.in_"+str(t)+"K")
    #
      commands.getoutput("./pwscf2force > config_"+str(t)+"K")
    else:
      commands.getoutput("cp data_fix.in_"+str(t)+"K data_fix.in")
      natom = commands.getoutput("awk '{if($2==\"atoms\"){print $1}}' data_fix.in")
      commands.getoutput(lammps_adress+" < in.lmp_fix")
    print "number of atoms: "+str(natom)

    # stress = pressure
    pxxl = commands.getoutput("awk '{if($1==\"pxxl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pyyl = commands.getoutput("awk '{if($1==\"pyyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pzzl = commands.getoutput("awk '{if($1==\"pzzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pxyl = commands.getoutput("awk '{if($1==\"pxyl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pxzl = commands.getoutput("awk '{if($1==\"pxzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pyzl = commands.getoutput("awk '{if($1==\"pyzl\"){printf \"%10.8f\",$3*7.4028083e-11}}' log.lammps")
    pxxp = commands.getoutput("awk '{if($1==\"#S\"){print $2}}' config_"+str(t)+"K")
    pyyp = commands.getoutput("awk '{if($1==\"#S\"){print $3}}' config_"+str(t)+"K")
    pzzp = commands.getoutput("awk '{if($1==\"#S\"){print $4}}' config_"+str(t)+"K")
    pxyp = commands.getoutput("awk '{if($1==\"#S\"){print $5}}' config_"+str(t)+"K")
    pxzp = commands.getoutput("awk '{if($1==\"#S\"){print $6}}' config_"+str(t)+"K")
    pyzp = commands.getoutput("awk '{if($1==\"#S\"){print $7}}' config_"+str(t)+"K")
    diffpxx = (float(pxxl) - float(pxxp))/(float(pxxp)+0.000000101)*100.0/6.0
    diffpyy = (float(pyyl) - float(pyyp))/(float(pyyp)+0.000000101)*100.0/6.0
    diffpzz = (float(pzzl) - float(pzzp))/(float(pzzp)+0.000000101)*100.0/6.0
    diffpxy = (float(pxyl) - float(pxyp))/(float(pxyp)+0.000000101)*100.0/6.0
    diffpxz = (float(pxzl) - float(pxzp))/(float(pxzp)+0.000000101)*100.0/6.0
    diffpyz = (float(pyzl) - float(pyzp))/(float(pyzp)+0.000000101)*100.0/6.0
    diffp = abs(diffpxx) + abs(diffpyy) + abs(diffpzz) + abs(diffpxy) + abs(diffpxz) + abs(diffpyz)
    print "lammps: "+str(pxxl)+", "+str(pyyl)+", "+str(pzzl)+", "+str(pxyl)+", "+str(pxzl)+", "+str(pyzl)+" [eV/A^3]"
    print "PWscf:  "+str(pxxp)+", "+str(pyyp)+", "+str(pzzp)+", "+str(pxyp)+", "+str(pxzp)+", "+str(pyzp)+" [eV/A^3]"
    print "P diff (%): "+str(diffp)
    print "---------------"

    # force
    difffx = 0.0
    difffy = 0.0
    difffz = 0.0
    difff  = 0.0
    for i in range(int(natom)):
      fxl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$7}}' trajectory.lammpstrj")
      fyl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$8}}' trajectory.lammpstrj")
      fzl[i] = commands.getoutput("awk '{if(NR==10+"+str(i)+"){printf \"%10.8f\",$9}}' trajectory.lammpstrj")
      fxp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $5}}' config_"+str(t)+"K")
      fyp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $6}}' config_"+str(t)+"K")
      fzp[i] = commands.getoutput("awk '{if(NR==11+"+str(i)+"){print $7}}' config_"+str(t)+"K")
      difffx = (float(fxl[i]) - float(fxp[i]))/(float(fxp[i])+0.000000101)*100.0/3.0/float(natom)
      difffy = (float(fyl[i]) - float(fyp[i]))/(float(fyp[i])+0.000000101)*100.0/3.0/float(natom)
      difffz = (float(fzl[i]) - float(fzp[i]))/(float(fzp[i])+0.000000101)*100.0/3.0/float(natom)
      difff  = difff + abs(difffx) + abs(difffy) + abs(difffz)
    print "lammps: "+str(fxl[0])+" : "+str(fyl[0])+" : "+str(fzl[0])+" [eV/A]"
    print "PWscf: "+str(fxp[0])+" : "+str(fyp[0])+" : "+str(fzp[0])+" [eV/A]"
    print "force diff (%): "+str(difff)
    print "---------------"

    lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%-20.10f\",$4}'"
    lmpe = commands.getoutput(lammps_get_data)

    pwe = commands.getoutput("awk '{if($1==\"#E\"){print $2}}' config_"+str(t)+"K")
    pwe = float(pwe) * float(natom)

    print "lammps: "+str(lmpe)+" [eV]"

    print "PWscf:  "+str(pwe)+" [eV]"

    diffe = float(pwe) - float(lmpe)
    print "diff: "+str(diffe)+" [eV]"
    diffea = float(diffe)/float(natom)
    print "diff/atom: "+str(diffea)+" [eV/atom]"
    commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")

    tdiffea = tdiffea + float(diffea)
    tdiffp  = tdiffp  + float(diffp)
    tdifff  = tdifff  + float(difff)
  
  diffb  = commands.getoutput("cat diff.dat")
  print "F boundary, diff: "+str(diffb)
  diffb  = commands.getoutput("cat diff.dat")

  print "---------------"
  
  y = 0.001/(float(tdiffea)**2 + 1000*float(diffb)**2 + 0.0000002*abs(tdiffp)**2 + 0.0000010*abs(tdifff)**2)

  print "Evaluate: ", y
  print "------------------------"

  return y
#----------------------------------------------------------------------
optimizer = BayesianOptimization(f=descripter, pbounds=pbounds)
optimizer.maximize(init_points=1, n_iter=6000, acq="ucb")
#acq = ucb, ei, poi, (default: ubc)

