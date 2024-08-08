#!/bin/bash

# slurm job script for slowing bar integration

#SBATCH --job-name=slowing_bar_hpc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
### added for parallelizing test ###
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --mem-per-cpu=5gb
#SBATCH --array=0-3
#SBATCH --partition=standard
#SBATCH --account=kjdaniel
#SBATCH --time=05:00:00
#SBATCH --output=/home/u21/rtolfree/job_outputs/slowing_bar/job_out_%x-%j-%A-%a.out
#SBATCH --mail-type=all
#SBATCH --mail-user=rtolfree@arizona.edu

module load python/3.11.4 
source ./functions/env_setup.sh
source ./envs/slowing_bar_hpc1/bin/activate
export PYTHONPATH="$PYTHONPATH:./functions"

#simulation setup
nsample=1000     # number of samples
nbatch=10       # number of batches of nsample orbits
simname="SlowDehnenBar_CR4_CR8"
startsimname="GrowDehnenBar_CR4"

# ENTER THE NUMBER OF ORBITS YOU WOULD LIKE TO INTEGRATE
number_of_starts_to_integrate=0
input="orbits/GrowDehnenBar_CR4/10000N_qiDF_MW14p_stklAA_orbits_cyl_GrowDehnenBar_CR4_0.npy"

tot_arr=4
:'
# This section runs start_setup and captures the necissary save dirs 
# for slurm maybe change python3 also change scriptdir
echo 'Starting_setup'
time python3 ./start_setup.py -n $nsample -nb $nbatch -sn $simname -ssn $startsimname
echo "Setup Complete"
# reads the .sh file with dir locs
source ./metadata/dirs.sh

########################################################
echo 
echo "Running TimeScaleCalc"
time python3 ./TimeScaleCalc.py -sn $simname -rmd $readme_dir -jd $json_dir
echo 'TimeScaleCalc Complete'
echo

source ./metadata/dirs1.sh

echo "Starting Integration"
time python3 ./integrate_orbits.py -sn $simname -rmd $readme_dir -jd $json_dir -in $inputs -n $nsample -nb $nbatch -a $tot_arr
echo "Integration complete"

# echo "Starting final NPY merge"
# time python3 ./merge_npy.py -jd $json_dir -a $tot_arr
# echo "Merge Complete"
'