from imports import argparse,json,np,Orbit,os
from dir_func import find_input_file
from joblib import Parallel, delayed, parallel_backend

from svptfncts import loadData
from TSolidBodyRotationWrapperPotential import TSolidBodyRotationWrapperPotential

# function to set up orbits for integration
def orbit_file_setup(inname,num_cpus,num_arrs,arr_id,num_stars):
    ICfile = np.load(inname)
    ICs = np.transpose(np.array([ICfile[0,:,-1],ICfile[3,:,-1],ICfile[4,:,-1],ICfile[2,:,-1],ICfile[5,:,-1],ICfile[1,:,-1]]))
    ICs=ICs[:num_stars]
    print(ICs.shape)

    # even deistributes arr into large bins based on how many array there are and assigns each arr a different set
    trim = ICs[:len(ICs)%num_arrs]
    print(trim)
    ICs=ICs[len(trim):]
    print(ICs.shape)
    ICs = ICs.reshape(num_arrs,-1,6)
    print(ICs.shape)
    ICs[0]=np.append(ICs[0],trim)
    print(ICs.shape)
    ICs = ICs[arr_id]

    trim = ICs[:len(ICs)%num_cpus]
    ICs=ICs[len(trim):]
    ICs = ICs.reshape(num_cpus,-1,6)
    ICs[0]=np.append(ICs[0],trim)
    # reshapes again based on cpus in node
    return ICs

# create parser for inital args
parser = argparse.ArgumentParser(description='Running Integration')
parser.add_argument('-rmd','--readmedir',type=str, nargs=1, help='Takes in the curr README dir')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir') 
parser.add_argument('-sn', '--simname', type=str, nargs=1, help='The name of the output folder.')
parser.add_argument('-n', '--nstars', type=int, nargs=1, help='The number of stars.')
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

# get input name
input_name=find_input_file('./!_Input','*.npy')

if input_name==-1:
    print('No Input File')
else:
# perform integration 
    # generate ICs
    input_name=str('./!_Input/'+input_name)
    ICs=orbit_file_setup(input_name,num_cpus,args['tot_arr'][0],arr_id,args['nstars'][0])
    print(ICs.shape)
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
    np.save(save_name,first_arr)

