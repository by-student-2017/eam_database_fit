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
pwscf_adress = "mpirun -np "+str(num_core)+" --allow-run-as-root pw.x"
#pwscf_adress = "mpirun -np "+str(num_core)+" pw.x"
#pwscf_adress = "mpirun -np 2 pw.x"

satom = commands.getoutput("grep \"atomtype\" EAM.input | sed -e \"s/.*=//\" -e \"s/'//g\"")

commands.getoutput("chmod +x ./cfg2vasp/cfg2vasp")
commands.getoutput("chmod +x pwscf2force")
commands.getoutput("chmod +x setinp")
commands.getoutput("./setinp")
#commands.getoutput("cp data.in data.in.origin")
commands.getoutput("mkdir cfg")
commands.getoutput("mkdir work")
commands.getoutput("echo -n > energy.dat")

temp_K = commands.getoutput("awk '{if($2==\"temp\"){print $4}}' in.lmp")
print "Lammps MD: "+temp_K+" K"

target = [0,0,0] # dummy data
y_str = [0] # dummy data

# fitting parameters
x0 = [2.54135105,
      1.56440565,
     21.31607638,
     21.50974615,
      7.73892498,
      4.36819705,
      0.39030193,
      0.5515945,
      0.31075621,
      0.76135587,
     -2.18416127,
     -0.2654721,
      1.09540177,
     -0.82252579,
     -2.20744692,
      0.56542599,
     -2.11301896,
      0.31236771,
     -2.20060466] # initial data
b1 = np.array([
    [2.000000,4.200000],
    [0.400000,4.200000],
    [5.700000,44.700000],
    [5.700000,44.700000],
    [5.700000,12.000000],
    [3.000000,6.500000],
    [0.100000,1.100000],
    [0.200000,1.700000],
    [0.100000,0.60],
    [0.200000,1.20],
    [-6.100000,-0.700000],
    [-2.500000,-0.030000],
    [-0.600000,1.9400000],
    [-5.300000,-0.550000],
    [-6.10,-0.70],
    [0.480000,3.600000],
    [-3.00000,0.930000],
    [0.300000,1.740000],
    [-6.100000,-0.66000]]) # boundary

count = 0
#----------------------------------------------------------------------
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", numpy.ndarray, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

n_gene = 19 # number of parameters
min_ind = numpy.ones(n_gene) * -1.0
max_ind = numpy.ones(n_gene) *  1.0
for i in range(n_gene):
  min_ind[i] = b1[i][0]
  max_ind[i] = b1[i][1]
  #print min_ind[i], max_ind[i]
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
  text = text.replace('F2',str(individual[15]).replace("[","").replace("]",""))
  text = text.replace('F3',str(individual[16]).replace("[","").replace("]",""))
  text = text.replace('eta',str(individual[17]).replace("[","").replace("]",""))
  text = text.replace('Fep',str(individual[18]).replace("[","").replace("]",""))
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

  y = 0.001/abs(diffea)

  print "Evaluate: ", y
  print "Parameters: ", individual
  print "------------------------"

  return y
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

