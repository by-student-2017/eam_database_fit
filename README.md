eam_database_fit


# Ubuntu 18.04 LTS
## Install (cif2cell-informal)
1. sudo apt install -y git python python-setuptools python-dev gcc
2. git clone https://github.com/by-student-2017/cif2cell-informal.git
3. cd cif2cell-informal
4. tar zxvf PyCifRW-3.3.tar.gz
5. cd PyCifRW-3.3
6. sudo python setup.py install
7. cd ..
8. sudo python setup.py install


## Install (lammps)
1. cd ~
2. sudo apt update
3. sudo apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
4. wget https://lammps.sandia.gov/tars/lammps-3Mar20.tar.gz
5. tar zxvf lammps-3Mar20.tar.gz
6. cd lammps-3Mar20
7. mkdir build ; cd build 
8. cmake -D BUILD_MPI=on -D PKG_USER-MEAMC=on -D PKG_MANYBODY=on -D PKG_MC=on ../cmake
9. cmake --build .


## Environment settings (lammps)
1. echo ' ' >> ~/.bashrc
2. echo '# lammps environment settings' >> ~/.bashrc
3. echo 'export PATH=$PATH:$HOME/lammps-3Mar20/build' >> ~/.bashrc
4. bash


## Install (PWscf)
1. cd ~
2. sudo apt update
3. sudo apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
4. wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
5. tar zxvf qe-6.4.1.tar.gz
6. cd q-e-qe-6.4.1
7. wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
8. patch -p1 --merge < backports-6.4.1.diff
9. ./configure
10. make pw
11. sudo make install


## set fitting 
1. cd ~
2. sudo apt update
3. sudo apt install -y git python-pip python-scipy csh gfortran gnuplot
4. git clone https://github.com/by-student-2017/eam_database_fit.git
5. cd ~/eam_database_fit
6. gfortran -o Zhou04_EAM_2 Zhou04_create_v2.f
7. gfortran -o plot plot.f


## fit parameters by Nelder-Mead (NM) method
1. cd ~/eam_database_fit
2. cp EAM.input_temp EAM.input
3. sed -i 's/Xx/Cu/g' EAM.input
4. cp in.lmp_temp_v2 in.lmp_temp
5. python nm_v5_debian.py
  or python nm_v4_debian.py
  (fit total energy, every force, every temperature and every structure)


## rewrite area (for nm_v5_debian.py)
1. gedit stract.dat


## fit parameters by other methods
1. cd ~/eam_database_fit
2. cp EAM.input_temp EAM.input
3. sed -i 's/Xx/Cu/g' EAM.input
4. cp in.lmp_temp_v2 in.lmp_temp
5. sed -i 's/YYYY/300.0/' in.lmp_temp
6. python nm.py


  (or python powell.py)


  (or python bfgs.py)


  (or python nm_v2.py) (fit total energy)


  (or python nm_v3.py) (fit total energy and every force)


## rewrite area
1. gedit nm_v4.py


temp = [77,273,1073,1573]


for t in temp:


  commands.getoutput("cp in.lmp in.lmp_"+str(t)+"K")


  commands.getoutput("sed -i 's/YYYY/"+str(t)+"/' in.lmp_"+str(t)+"K")


  commands.getoutput("cp data.in data.in_"+str(t)+"K")


#if you would set other structures, e.g.,


#commands.getoutput("cp data.in data.in_77K")


#commands.getoutput("cp data.in data.in_273K")


#commands.getoutput("cp ./data/data.in.BCC data.in_1073K")


#commands.getoutput("cp ./data/data.in.HCP data.in_1578K")


## fit parameters by genetic algorithm
1. cd ~/eam_database_fit
2. pip install -U deap --user
3. cp EAM.input_temp EAM.input
4. sed -i 's/Xx/Cu/g' EAM.input
5. cp in.lmp_temp_v2 in.lmp_temp
6. sed -i 's/YYYY/300.0/' in.lmp_temp
7. python ga.py


## fit parameters by baysian method
1. cd ~/eam_database_fit
2. pip install bayesian-optimization==1.1.0
3. cp EAM.input_temp EAM.input
4. sed -i 's/Xx/Cu/g' EAM.input
5. cp in.lmp_temp_v2 in.lmp_temp
6. sed -i 's/YYYY/300.0/' in.lmp_temp
7. python baysian.py


## fit parameters by Particle Swarm Optimization (PSO)
1. cd ~/eam_database_fit
2. pip2 install pyswarm==0.6
3. cp EAM.input_temp EAM.input
4. sed -i 's/Xx/Cu/g' EAM.input
5. gedit struct.dat
6. python pyswarm_v6_debian.py


## fit parameters by Particle Swarm Optimization (PSO)
1. cd ~/eam_database_fit
2. pip2 install miniful
3. pip2 install fst-pso==1.7.5
4. cp EAM.input_temp EAM.input
5. sed -i 's/Xx/Cu/g' EAM.input
6. gedit struct.dat
7. python fstpso_v6_debian.py


## plot F, rho or z2r
1. gnuplot png.gp


# Google Colaboratory
## Install (cif2cell-informal)
	!apt update
	!apt install -y git python python-setuptools python-dev gcc
	%cd /content
	!git clone https://github.com/by-student-2017/cif2cell-informal.git
	%cd cif2cell-informal
	!tar zxvf PyCifRW-3.3.tar.gz
	%cd PyCifRW-3.3
	!python2 setup.py install
	%cd /content/cif2cell-informal
	!python2 setup.py install


## Install (lammps)
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://lammps.sandia.gov/tars/lammps-3Mar20.tar.gz
	!tar zxvf lammps-3Mar20.tar.gz
	%cd lammps-3Mar20
	!mkdir build
	%cd build 
	!cmake -D BUILD_MPI=on -D PKG_USER-MEAMC=on -D PKG_MANYBODY=on -D PKG_MC=on ../cmake
	!cmake --build .
	import os
	os.environ['PATH'] = "/content/lammps-3Mar20/build:"+os.environ['PATH']


## Install (PWscf)
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
	!tar zxvf qe-6.4.1.tar.gz
	%cd q-e-qe-6.4.1
	!wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
	!patch -p1 --merge < backports-6.4.1.diff
	!./configure
	!make pw
	import os
	os.environ['PATH'] = "/content/q-e-qe-6.4.1/bin:"+os.environ['PATH']


## set fitting
	!apt update
	!apt install -y git python-pip python-scipy csh gfortran gnuplot
	%cd /content
	!git clone https://github.com/by-student-2017/eam_database_fit.git
	%cd /content/eam_database_fit
	!gfortran -o Zhou04_EAM_3 Zhou04_create_v3.f
	!gfortran -o plot plot.f


## fit parameters by Nelder-Mead (NM) method
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!python2 nm_v5_gc.py
	!cat EAM_code


	(or !python nm_v4_gc.py) (fit total energy, every force, every temperature and every structure)


## fit parameters by other methods
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!sed -i 's/YYYY/300.0/' in.lmp_temp
	!python2 nm_gc.py
	!cat EAM_code
	
	or !python2 powell_gc.py
	
	or !python2 bfgs_gc.py
	
	(or !python nm_v2_gc.py) (fit total energy)
	
	(or !python nm_v3_gc.py) (fit total energy and every force)


## fit parameters by genetic algorithm
	!pip2 install -U deap --user
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!python2 ga_v6_gc.py
	!cat EAM_code


## fit parameters by baysian method
	!pip2 install bayesian-optimization==1.1.0
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!python2 baysian_v6_gc.py
	!cat EAM_code


## fit parameters by genetic algorithm
	!pip2 install -U deap --user
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!sed -i 's/YYYY/300.0/' in.lmp_temp
	!python2 ga_gc.py
	!cat EAM_code


## fit parameters by baysian method
	!pip2 install bayesian-optimization==1.1.0
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!cp in.lmp_temp_v2 in.lmp_temp
	!sed -i 's/YYYY/300.0/' in.lmp_temp
	!python2 baysian_gc.py
	!cat EAM_code


## fit parameters by Particle Swarm Optimization (PSO)
	!pip2 install pyswarm==0.6
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!python2 pyswarm_v6_gc.py
	!cat EAM_code


## fit parameters by Particle Swarm Optimization (PSO)
	!pip2 install miniful
	!pip2 install fst-pso==1.7.5
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!python2 fstpso_v6_gc.py
	!cat EAM_code


## fit parameters by NM method
	%cd /content/eam_database_fit
	!cp ./EAM_fit_v3/EAM_code_v3.init ./
	!cp ./EAM_fit_v3/EAM_code_v3.temp ./
	!cp ./EAM_fit_v3/nm_v31_gc.py ./
	!cp ./EAM_fit_v3/Zhou04_create_v31.f ./
	!cp ./EAM_fit_v3/setinp ./
	!cp ./EAM_fit_v3/struct.dat ./
	!gfortran -o Zhou04_EAM_v31 Zhou04_create_v31.f
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Li/g' EAM.input
	!python2 nm_v31_gc.py
	!cat EAM_code_v3


## fit parameters by NM method
	!cp ./EAM_fit_v3/EAM_code_v32.init ./
	!cp ./EAM_fit_v3/EAM_code_v32.temp ./
	!cp ./EAM_fit_v3/nm_v32_gc.py ./
	!cp ./EAM_fit_v3/Zhou04_create_v32.f ./
	!cp ./EAM_fit_v3/setinp ./
	!cp ./EAM_fit_v3/struct.dat ./
	!gfortran -o Zhou04_EAM_v32 Zhou04_create_v32.f
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Zn/g' EAM.input
	!python2 nm_v32_gc.py
	!cat EAM_code_v32


## plot F, rho or z2r
	!gnuplot png.gp


## all settings
	!apt update
	!apt install -y git python python-setuptools python-dev gcc
	%cd /content
	!git clone https://github.com/by-student-2017/cif2cell-informal.git
	%cd cif2cell-informal
	!tar zxvf PyCifRW-3.3.tar.gz
	%cd PyCifRW-3.3
	!python2 setup.py install
	%cd /content/cif2cell-informal
	!python2 setup.py install
	
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://lammps.sandia.gov/tars/lammps-3Mar20.tar.gz
	!tar zxvf lammps-3Mar20.tar.gz
	%cd lammps-3Mar20
	!mkdir build
	%cd build 
	!cmake -D BUILD_MPI=on -D PKG_USER-MEAMC=on -D PKG_MANYBODY=on -D PKG_MC=on ../cmake
	!cmake --build .
	import os
	os.environ['PATH'] = "/content/lammps-3Mar20/build:"+os.environ['PATH']
	
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://github.com/QEF/q-e/archive/qe-6.4.1.tar.gz
	!tar zxvf qe-6.4.1.tar.gz
	%cd q-e-qe-6.4.1
	!wget https://github.com/QEF/q-e/releases/download/qe-6.4.1/backports-6.4.1.diff
	!patch -p1 --merge < backports-6.4.1.diff
	!./configure
	!make pw
	import os
	os.environ['PATH'] = "/content/q-e-qe-6.4.1/bin:"+os.environ['PATH']
	
	!apt update
	!apt install -y git python-pip python-scipy csh gfortran gnuplot
	%cd /content
	!git clone https://github.com/by-student-2017/eam_database_fit.git
	%cd /content/eam_database_fit
	!gfortran -o Zhou04_EAM_3 Zhou04_create_v3.f
	!gfortran -o plot plot.f
	
	!pip2 install pyswarm==0.6
	%cd /content/eam_database_fit
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!cp EAM.input_temp EAM.input
	!sed -i 's/Xx/Cu/g' EAM.input
	!python2 pyswarm_v6_gc.py
	!cat EAM_code