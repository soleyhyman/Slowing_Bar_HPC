from imports import argparse,np,json,os,shutil
import time
# create parser for inital args
parser = argparse.ArgumentParser(description='Running Integration')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir')
parser.add_argument('-ar','--tot_arr',type=int,nargs=1,help='Takes total arrs') 
args = vars(parser.parse_args())

 # open json to get necissary file paths
with open(args['jsondir'][0],'r') as json_file:
    data=json.load(json_file)
    dir_data=data['dir_data']

# moves file from input to input dir
try:
    shutil.move(dir_data['input_file_name'], dir_data['inputdir'])
except:
    print('File could not be moved from input.')

# gets a type for each different kind of info
for type in range(3):
    kinds=['cyl','cart','action']
    init_name=f"{dir_data['outdir']}/{dir_data['sim_name_full']}_{kinds[type]}"
    # combine arrs
    results=np.load(f"{init_name}_0.npy")
    for x in range(args['tot_arr'][0]):
        if x ==0:
            pass
        else:
            curr_name=f"{init_name}_{x}.npy"
            curr_arr=np.load(curr_name)
            results=np.concatenate((results,curr_arr),axis=0)
        os.remove(f"{init_name}_{x}.npy")
    np.save(init_name,results)