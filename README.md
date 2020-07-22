# eam_database_ga_fit


# fit parameter on genetic algorithm


# Ubuntu 18.04 LTS or Debian 10.0
## Install (lammps)
1. cd ~
2. sudo apt update
3. sudo apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
4. wget https://lammps.sandia.gov/tars/lammps-stable.tar.gz
5. tar zxvf lammps-stable.tar.gz
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


## Run
1. cd ~
2. sudo apt update
3. sudo apt install -y git python-pip
4. git clone https://github.com/by-student-2017/eam_database_ga_fit.git
5. cd ~/eam_database_ga_fit
6. gfortran create.f -o gen_eam
7. pip install -U deap --user
8. gedit data.in
9. gedit EAM.input
10. gedit EAM_code
11. python ga.py


# Google Colaboratory
## Install (lammps)
	!apt update
	!apt install -y gcc g++ build-essential gfortran libopenblas-dev libfftw3-dev libopenmpi-dev wget
	%cd /content
	!wget https://lammps.sandia.gov/tars/lammps-stable.tar.gz
	!tar zxvf lammps-stable.tar.gz
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


## Run
	!apt update
	!apt install -y git python2-pip
	%cd /content
	!git clone https://github.com/by-student-2017/eam_database_ga_fit.git
	%cd /content/eam_database_ga_fit
	!gfortran create.f -o gen_eam
	!pip install -U deap --user
	import os
	os.environ["OMP_NUM_THREADS"] = "1,1"
	os.environ["MKL_NUM_THREADS"] = "1"
	!python2 ga.py