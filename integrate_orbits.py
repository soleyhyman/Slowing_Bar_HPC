from imports import argparse,json,np,Orbit,os,Pool
from dir_func import get_unique_filename, create_directories
from joblib import Parallel, delayed, parallel_backend

from svptfncts import loadData,saveData
from TSolidBodyRotationWrapperPotential import TSolidBodyRotationWrapperPotential

# function to set up orbits for integration
def orbit_file_setup(inname,num_cpus,num_arrs,arr_id):
    ICfile = np.load(inname)
    ICs = np.transpose(np.array([ICfile[0,:,-1],ICfile[3,:,-1],ICfile[4,:,-1],ICfile[2,:,-1],ICfile[5,:,-1],ICfile[1,:,-1]]))
    # even deistributes arr into large bins based on how many array there are and assigns each arr a different set
    ICs = ICs.reshape(num_arrs,(len(ICs)//num_arrs),6)
    ICs = ICs[arr_id]
    ICs = ICs.reshape(num_cpus,(len(ICs)//num_cpus),6)
    # reshapes again based on cpus in node
    return ICs

# create parser for inital args
parser = argparse.ArgumentParser(description='Running Integration')
parser.add_argument('-rmd','--readmedir',type=str, nargs=1, help='Takes in the curr README dir')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir') 
parser.add_argument('-sn', '--simname', type=str, nargs=1, help='The name of the output folder.')
parser.add_argument('-in','--inputname',type=str,nargs=1,help='This takes the input dir')
parser.add_argument('-n', '--nstars', type=int, nargs=1, help='The number of stars per batch.')
parser.add_argument('-nb', '--nbatch', type=int, nargs=1, help='The number of batches.')
parser.add_argument('-a', '--tot_arr',type=int,nargs=1, help='The total number of arrays in array job.')
args = vars(parser.parse_args())

# open json to get necissary file paths
with open(args['jsondir'][0],'r') as json_file:
    data=json.load(json_file)
    dir_data=data['dir_data']
    # load pickled objs
    diskmodel=loadData(data['dir_data']['dm_name'])
    dehnenBarModel_Omega=loadData(data['dir_data']['dbo_name'])
    # gets dicts of info
    diskmodel_data=diskmodel.get_params()
    dehnenBarModel_Omega_data=dehnenBarModel_Omega.get_params()

# recreate TSlowNat
# set adiquite timestamps 
TSlowNat = loadData(data['dir_data']['TSlowNat_dir'])

# create btp
btp = TSolidBodyRotationWrapperPotential(pot=dehnenBarModel_Omega_data['bp_still'],omegai=dehnenBarModel_Omega_data['omegaBi'],
                                         omegaf=dehnenBarModel_Omega_data['omegaBf'],to=dehnenBarModel_Omega_data['to'],tsteady=TSlowNat,pa=0.)

# find the num of cpus
num_cpus = int(os.environ["SLURM_CPUS_ON_NODE"]) 

# find arr num for arr job
arr_id = int(os.environ["SLURM_ARRAY_TASK_ID"])

# create pot
pot=[diskmodel_data['mwp'],btp]

# pull nphio
nphio=np.load(dir_data['tphio_dir'])
tvector=np.load(dir_data['tvector_dir'])

# perform integration 
ICs=orbit_file_setup(args['inputname'][0],num_cpus,args['tot_arr'][0],arr_id)

# integration_func
def integration_loop(index):
    orbits=Orbit(ICs[index])
    orbits.integrate(tvector,pot,method='leapfrog')
    orp = np.array([orbits.R(tvector),
                orbits.phi(tvector),
                orbits.z(tvector),
                orbits.vR(tvector),
                orbits.vT(tvector),
                orbits.vz(tvector)])
    # moves orp so that its organized by orbit - timestamps - cords
    orp=orp.transpose(1,2,0)
    save_name=f"{dir_data['outdir']}/{dir_data['sim_name_full']}_{arr_id}_{index}.npy"
    np.save(save_name,orp)
    del(orbits)
    return [index,save_name]

# integration_loop
with parallel_backend('loky',n_jobs=num_cpus):
    with Parallel(n_jobs=num_cpus) as parallel:
        names = parallel(delayed(integration_loop)(i) for i in range(len(ICs)))
print(names)
# merges all this arrs nmpys into one
first_arr=np.load(names[0][1])
for x in range(len(names)):
    if x ==0:
        pass 
    else:
        curr=np.load(names[x][1])
        first_arr=np.concatenate((first_arr,curr),axis=0)
    os.remove(names[x][1])
save_name=f"{dir_data['outdir']}/{dir_data['sim_name_full']}_{arr_id}.npy"
print(first_arr.shape)
np.save(save_name,first_arr)

