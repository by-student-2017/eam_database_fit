#!/bin/bash

for atom in La Yb Hf Sb Bi
do
  cp EAM.input_temp EAM.input
  sed -i 's/Xx/'${atom}'/g' EAM.input
  cp in.lmp_temp_v2 in.lmp_temp
  sed -i 's/YYYY/300.0/' in.lmp_temp
  python nm_debian.py
  mv config_potfit config_potfit_${atom}_300K
  mv energy.dat energy_${atom}_300K.dat
  mv EAM_code EAM_code_${atom}_300K.dat
  echo -n > config_potfit
  echo -n > energy.dat
done
end
