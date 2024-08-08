from imports import argparse,np,json,os
import time
# create parser for inital args
parser = argparse.ArgumentParser(description='Running Integration')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir') 
parser.add_argument('-a','--tot_arr',type=int, nargs=1,help='Takes the total arrs in array job')
args = vars(parser.parse_args())

# find arr num for arr job
arr_id = int(os.environ["SLURM_ARRAY_TASK_ID"])

if arr_id==0:
    # sleep 
    time.sleep(600)

    # open json to get necissary file paths
    with open(args['jsondir'][0],'r') as json_file:
        data=json.load(json_file)
        dir_data=data['dir_data']

    init_name=f"{dir_data['outdir']}/{dir_data['sim_name_full']}"
    # combine arrs
    results=np.load(f"{dir_data['outdir']}/{dir_data['sim_name_full']}_0.npy")
    for x in range(args['tot_arr'][0]):
        if x ==0:
            pass
        else:
            curr_name=f"{init_name}_{x}.npy"
            curr_arr=np.load(curr_name)
            results=np.concatenate((results,curr_arr),axis=0)
        os.remove(f"{init_name}_{x}.npy")
    np.save(init_name,results)