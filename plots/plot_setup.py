from imports import argparse,json
from svptfncts import loadData
# create parser for inital args
parser = argparse.ArgumentParser(description='Creating Plots')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir') 
args = vars(parser.parse_args())

# open the json file to get shared data
with open(args['jsondir'][0],'r') as json_file:
    data=json.load(json_file)

# load pickled objs
diskmodel=loadData(data['dir_data']['dm_name'])
dehnenBarModel_Omega=loadData(data['dir_data']['dbo_name'])
# gets dicts of info
diskmodel_data=diskmodel.get_params()
dehnenBarModel_Omega_data=dehnenBarModel_Omega.get_params()

plot_params= {
    'rscale' : 1.*8.,
    'vscale' : 1.*220.,


}