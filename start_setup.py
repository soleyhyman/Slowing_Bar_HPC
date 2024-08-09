from imports import json, argparse, datetime, __version__, timezone,os,np
from DiskModel_obj import DiskModel_obj
from dbm_omega_obj import dbm_omega_obj
from create_readMe import diskmodel_readme, dehnen_readme
from dir_func import create_directories, get_unique_filename, json_serialize_full, get_current_time_dhm,find_input_file
from svptfncts import saveData

#create parser to get arguments from sh
parser = argparse.ArgumentParser(description='Creating README and making necissary directories.')
parser.add_argument('-n', '--nstars', type=int, nargs=1, help='The number of stars.')
parser.add_argument('-sn', '--simname', type=str, nargs=1, help='The name of the output folder.')
parser.add_argument('-ssn', '--startsimname', type=str, nargs=1, help='The name of the folder holding inital data.')
# parser.add_argument('-rmin', '--rmin', type=float, nargs=1, help='Value of rmin.')
# parser.add_argument('-rmax', '--rmax', type=float, nargs=1, help='Value of rmax.')
# parser.add_argument('-zmax', '--zmax', type=float, nargs=1, help='Value of zmax.')
args = vars(parser.parse_args())

# create orbit dir
create_directories('./orbits')

# create output dir
create_directories(f"./orbits/{str(args['simname'][0])}")

#create input dir
create_directories(f"./orbits/{str(args['startsimname'][0])}")

# create README dir
create_directories('./READMEs')

#create metadata dir
create_directories('./metadata')

#create pickle dir
create_directories('./metadata/pickles')

# determines file name based on how many stars are chosen
if args['nstars'][0]==-1:
    input_name=find_input_file('./!_Input','*.npy')
    arr=np.load(input_name)
    nstars=arr.shape[1]
    del arr
else:
    nstars=args['nstars'][0]

# setup sim params 
sim_params = {
    'nstars' : nstars,
    'rmin' : 0.0125, 
    'rmax' : 1.25,      
    'zmax' : 0.3 
}

########## Create the DiskModel and DehnenBar_Omega objs ##########
diskmodel=DiskModel_obj()
dehnenbar_omega=dbm_omega_obj()

# take the vars and clean them for json
dm_clean,dm_dirty=json_serialize_full(diskmodel.get_params())
dbo_clean,dbo_dirty=json_serialize_full(dehnenbar_omega.get_params())

#set up dir data
dir_data = {
    "outdir" : f"./orbits/{str(args['simname'][0])}",
    'inputdir' : f"./orbits/{str(args['startsimname'][0])}",
    'sim_name_full': f"{args['startsimname'][0]}_{sim_params['nstars']}_{get_current_time_dhm()}"
}

# create unique filename
json_filename = f"{dir_data['sim_name_full']}"
json_unique = get_unique_filename(json_filename,'json','./metadata')

# create README name
rmfile = f"{dir_data['sim_name_full']}_README"
rmfile_unique = get_unique_filename(rmfile,'txt','./READMEs')

# add file names to dir_data
dir_data['rmfile_dir'] = rmfile_unique
dir_data['json_dir'] = json_unique 

# pickle diskmodel and dehnenbar objs for TimeScale and other files
dm_name=get_unique_filename(f'diskmodel_obj_{get_current_time_dhm()}_','pickle','./metadata/pickles')
dbo_name=get_unique_filename(f'dehnenbar_omega_obj_{get_current_time_dhm()}_','pickle','./metadata/pickles')
saveData(diskmodel,dm_name)
saveData(dehnenbar_omega,dbo_name)

# add pickle dirs to json
dir_data['dm_name']=dm_name
dir_data['dbo_name']=dbo_name

#set up json data
json_data = {
    'dir_data' : dir_data,
    'sim_params' : sim_params,
    'diskmodel_data' : dm_clean,
    'dehnenBarModel_Omega_data': dbo_clean,
}

# create json
with open(json_unique, 'w') as json_file:
    json.dump(json_data,json_file, indent=4)

if int(os.environ["SLURM_ARRAY_TASK_ID"])==0:
    # create README
    with open(rmfile_unique, 'w') as rm:
        rm.write('Slowing Bar Integration\n\n')
        rm.write('Made by Dr. Kate Daniel and Rowan Tolfree\n')
        rm.write('-----------------------------------------\n')
        rm.write('##### ADD A DESCRIPTION #####\n')
        rm.write('-----------------------------------------\n\n')
        rm.write(f"Created: {str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))}\n")
        rm.write(f"Galpy {__version__}")    
        rm.write('\n\n')

    # add diskmodel and dehnen to readme 
    diskmodel_readme(json_unique)
    dehnen_readme(json_unique)

    # writes dirs to a .sh file to bring up to the running shell
    with open('metadata/dirs.sh', 'w') as f:
        f.write(f"input_dir={dir_data['inputdir']}\n")
        f.write(f"output_dir={dir_data['outdir']}\n")
        f.write(f"json_dir={dir_data['json_dir']}\n")
        f.write(f"readme_dir={dir_data['rmfile_dir']}\n")
        f.write(f"dm_name={dm_name}\n")
        f.write(f"dbo_name={dbo_name}\n")
