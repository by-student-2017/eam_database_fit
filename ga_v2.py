import random
from deap import creator, base, tools, algorithms
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
#print "initial parameters: ",x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21
x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21]
print "initial parameters: ",x

count = 0
#----------------------------------------------------------------------
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

n_gene = 22 # number of parameters
min_ind = numpy.ones(n_gene) * -1.0
max_ind = numpy.ones(n_gene) *  1.0
for i in range(n_gene):
  #min_ind[i] = b1[i][0]
  #max_ind[i] = b1[i][1]
  min_ind[i] = float(x[i]) - float(x[i])*0.1
  max_ind[i] = float(x[i]) + float(x[i])*0.1
  print "search area of paramter "+str(i)+": "+str(min_ind[i])+" | "+str(max_ind[i])
#----------------------------------------------------------------------
def create_ind_uniform(min_ind, max_ind):
  ind = []
  for min, max in zip(min_ind, max_ind):
    ind.append(random.uniform(min, max))
  return ind
#----------------------------------------------------------------------
toolbox.register("create_ind", create_ind_uniform, min_ind, max_ind)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_ind)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#----------------------------------------------------------------------
#def evalOneMax(individual):
#  return sum(individual),
#----------------------------------------------------------------------
def evalOneMax(individual):
  
  print "------------------------"
  global count
  count += 1
  print count

  fi = open(file_tmp,'r')
  text = fi.read().replace('re',str(individual[0]).replace("[","").replace("]",""))
  text = text.replace('fe',str(individual[1]).replace("[","").replace("]",""))
  text = text.replace('rhoe1',str(individual[2]).replace("[","").replace("]",""))
  text = text.replace('rhoe2',str(individual[3]).replace("[","").replace("]",""))
  text = text.replace('alpha',str(individual[4]).replace("[","").replace("]",""))
  text = text.replace('beta',str(individual[5]).replace("[","").replace("]",""))
  text = text.replace('Ap',str(individual[6]).replace("[","").replace("]",""))
  text = text.replace('Bp',str(individual[7]).replace("[","").replace("]",""))
  text = text.replace('kappa',str(individual[8]).replace("[","").replace("]",""))
  text = text.replace('lambda',str(individual[9]).replace("[","").replace("]",""))
  text = text.replace('Fn0',str(individual[10]).replace("[","").replace("]",""))
  text = text.replace('Fn1',str(individual[11]).replace("[","").replace("]",""))
  text = text.replace('Fn2',str(individual[12]).replace("[","").replace("]",""))
  text = text.replace('Fn3',str(individual[13]).replace("[","").replace("]",""))
  text = text.replace('F0',str(individual[14]).replace("[","").replace("]",""))
  text = text.replace('F1',str(individual[15]).replace("[","").replace("]",""))
  text = text.replace('F2',str(individual[16]).replace("[","").replace("]",""))
  text = text.replace('F3',str(individual[17]).replace("[","").replace("]",""))
  text = text.replace('eta',str(individual[18]).replace("[","").replace("]",""))
  text = text.replace('Fep',str(individual[19]).replace("[","").replace("]",""))
  text = text.replace('F4',str(individual[20]).replace("[","").replace("]",""))
  text = text.replace('rhol',str(individual[21]).replace("[","").replace("]",""))
  fi.close

  with open(file_inp,'w') as f:
    print >> f, text

  commands.getoutput("./Zhou04_EAM_2 < EAM.input")
  if (count % 3000) == 1: 
    commands.getoutput(lammps_adress+" < in.lmp")
    commands.getoutput("cp ./cfg/run.50.cfg run.50.cfg")
    commands.getoutput("./cfg2vasp/cfg2vasp run.50.cfg")
    commands.getoutput("python ./vasp2cif/vasp2cif.py run.50.vasp")
    commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.48 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
    commands.getoutput(pwscf_adress+" < pw.scf.in")
    commands.getoutput(cif2cell_adress+" run.50.vasp.cif --no-reduce -p pwscf --pwscf-pseudo-PSLibrary-libdr=\"./potentials\" --setup-all --k-resolution=0.18 --pwscf-force=yes --pwscf-stress=yes --pwscf-run-type=scf -o pw.in") 
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
  diffpxx = (float(pxxl) - float(pxxp))/(float(pxxp)+0.000000101)*100.0/6.0
  diffpyy = (float(pyyl) - float(pyyp))/(float(pyyp)+0.000000101)*100.0/6.0
  diffpzz = (float(pzzl) - float(pzzp))/(float(pzzp)+0.000000101)*100.0/6.0
  diffpxy = (float(pxyl) - float(pxyp))/(float(pxyp)+0.000000101)*100.0/6.0
  diffpxz = (float(pxzl) - float(pxzp))/(float(pxzp)+0.000000101)*100.0/6.0
  diffpyz = (float(pyzl) - float(pyzp))/(float(pyzp)+0.000000101)*100.0/6.0
  diffp = abs(diffpxx) + abs(diffpyy) + abs(diffpzz) + abs(diffpxy) + abs(diffpxz) + abs(diffpyz)
  print "lammps: "+str(pxxl)+", "+str(pyyl)+", "+str(pzzl)+", "+str(pxyl)+", "+str(pxzl)+", "+str(pyzl)+" [eV/A^3]"
  print "pwscf:  "+str(pxxp)+", "+str(pyyp)+", "+str(pzzp)+", "+str(pxyp)+", "+str(pxzp)+", "+str(pyzp)+" [eV/A^3]"
  print "P diff (%): "+str(diffp)
  print "---------------"

  lammps_get_data = "grep \"Total Energy\" log.lammps | tail -1 | awk '{printf \"%-20.10f\",$4}'"
  lmpe = commands.getoutput(lammps_get_data)

  pwe = commands.getoutput("awk '{if($1==\"#E\"){print $2}}' config")
  pwe = float(pwe) * float(natom)

  print "lammps: "+str(lmpe)+" [eV]"

  print "PWscf:  "+str(pwe)+" [eV]"

  diffe = float(pwe) - float(lmpe)
  print "diff: "+str(diffe)+" [eV]"
  diffea = float(diffe)/float(natom)
  print "diff/atom: "+str(diffea)+" [eV/atom]"
  commands.getoutput("echo "+str(count)+" "+str(diffe)+" >> energy.dat")

  rhoin  = float(individual[2])*float(individual[21])
  rhoout = float(individual[2])*1.15
  print "---------------"
  print "F boundary 1, rho: "+str(rhoin)
  print "F boundary 2, rho: "+str(individual[2])
  print "F boundary 3, rho: "+str(rhoout)
  commands.getoutput("cp "+satom+"_Zhou04.eam.alloy"+" Xx_Zhou04.eam.alloy")
  commands.getoutput("./plot")
  rhoin1  = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoin)+"){print $2}}' | tail -2 | head -1")
  rhoin2  = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoin)+"){print $2}}' | head -2 | tail -1")
  rhoe1   = commands.getoutput("cat F.plt | awk '{if($1<"+str(individual[2])+"){print $2}}' | tail -2 | head -1")
  rhoe2   = commands.getoutput("cat F.plt | awk '{if($1>"+str(individual[2])+"){print $2}}' | head -2 | tail -1")
  rhoout1 = commands.getoutput("cat F.plt | awk '{if($1<"+str(rhoout)+"){print $2}}' | tail -2 | head -1")
  rhoout2 = commands.getoutput("cat F.plt | awk '{if($1>"+str(rhoout)+"){print $2}}' | head -2 | tail -1")
  print "F near boundary 1, F: "+str(rhoin1)+" | "+str(rhoin2)+" | diff "+str(float(rhoin1) - float(rhoin2))
  print "F near boundary 2, F: "+str(rhoe1)+" | "+str(rhoe2)+" | diff "+str(float(rhoe1) - float(rhoe2))
  print "F near boundary 3, F: "+str(rhoout1)+" | "+str(rhoout2)+" | diff "+str(float(rhoout1) - float(rhoout2))
  print "---------------"

  y = 0.001/(abs(diffea)**2 + 1000*abs(float(rhoin1) - float(rhoin2))**2 + 1000*abs(float(rhoe1) - float(rhoe2))**2 + 1000*abs(float(rhoout1) - float(rhoout2))**2 + 0.0000002*abs(diffp)**2)

  print "Evaluate: ", y
  #print "Parameters: ", individual
  print "Parameters: x0 = "+"[ "+str(individual[0])+","+str(individual[1])+","+str(individual[2])+","+str(individual[3])+","+str(individual[4])+","+str(individual[5])+","+str(individual[6])+","+str(individual[7])+","+str(individual[8])+","+str(individual[9])+","+str(individual[10])+","+str(individual[11])+","+str(individual[12])+","+str(individual[13])+","+str(individual[14])+","+str(individual[15])+","+str(individual[16])+","+str(individual[17])+","+str(individual[18])+","+str(individual[19])+","+str(individual[20])+","+str(individual[21])+" ]"
  print "------------------------"

  return y,
#----------------------------------------------------------------------
def cxTwoPointCopy(ind1, ind2):
  size = len(ind1)
  cxpoint1 = random.randint(1, size)
  cxpoint2 = random.randint(1, size-1)
  if (cxpoint2 >= cxpoint1):
    cxpoint2 += 1
  else:
    cxpoint1, cxpoint2 = cxpoint2, cxpoint1

  ind1[cxpoint1:cxpoint2], ind2[cxpoint2:cxpoint2] = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

  return ind1, ind2
#----------------------------------------------------------------------
def mutUniformDbl(individual, min_ind, max_ind, indpb):
  size = len(individual)
  for i, min, max in zip(xrange(size), min_ind, max_ind):
    if (random.random() < indpb):
      individual[i] = random.uniform(min, max)
  return indivisual,
#----------------------------------------------------------------------
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
#----------------------------------------------------------------------
def main():
  random.seed(64)
  pop = toolbox.population(n=300)
  hof = tools.HallOfFame(1, similar=numpy.array_equal)
  stats = tools.Statistics(lambda ind: ind.fitness.values)
  stats.register("avg", numpy.mean)
  stats.register("std", numpy.std)
  stats.register("min", numpy.min)
  stats.register("max", numpy.max)
  algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50000, stats=stats, halloffame=hof)
  return pop, stats, hof
#----------------------------------------------------------------------
if (__name__ == "__main__"):
  main()
#----------------------------------------------------------------------

