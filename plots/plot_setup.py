from imports import argparse,json,np,lindbladR,brentq,omegac,verticalfreq,u
from svptfncts import loadData
from dir_func import dir_layer_out

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


rscale= 1.*8.
vscale= 1.*220.
m=2
nbeg:0
ntest= -1
mwp= diskmodel_data['mwp']
omegat=np.load(f"{dir_layer_out(1,data['dir_data']['omegat_dir'])}")

mwILR = lindbladR(mwp,omegatend,m=m)*rscale
mwOLR = lindbladR(mwp,omegatend,m=-m)*rscale
mwUILR = lindbladR(mwp,omegatend,m=m*2)*rscale
mwUOLR = lindbladR(mwp,omegatend,m=-m*2)*rscale
mwCR = lindbladR(mwp,omegatend,m='corotation')*rscale

def vertres_eq(R,Pot,OmegaP,m,t=0):
    return m*(omegac(Pot,R)-OmegaP)-verticalfreq(Pot,R)

vi11 = brentq(vertres_eq,0.0000001,1000.,args=(mwp,omegatend,m))*rscale
vi12 = brentq(vertres_eq,0.0000001,1000.,args=(mwp,omegatend,m*2))*rscale
vo11 = brentq(vertres_eq,0.0000001,1000.,args=(mwp,omegatend,-m))*rscale
vo12 = brentq(vertres_eq,0.0000001,1000.,args=(mwp,omegatend,-m*2))*rscale

### Specify simulation info for plot titles
titlewords = 'N = '+str(data['sim_params']['nstars'])+', R_CR = '+str(np.round(mwCR,2)*u.kpc)+', iteration = '+iteration
labelwords = '\n'.join((
    r'$N=%d$' % (data['sim_params']['nstars']),
    r'$R_{CR}=%.2f$ kpc' % (mwCR, ),
    r'$Iteration=%d$' % (itr, )))

### Upload orbital info
orbits = np.load('../3_SlowBar/orbits/'+simname+'/10000N_qiDF_MW14p_stklAA_orbits_cart_'+simname+'_'+iteration+'.npy')  
orbitc = np.load('../3_SlowBar/orbits/'+simname+'/10000N_qiDF_MW14p_stklAA_orbits_cyl_'+simname+'_'+iteration+'.npy')  
actions = np.load('../3_SlowBar/orbits/'+simname+'/10000N_qiDF_MW14p_stklAA_actions_'+simname+'_'+iteration+'.npy')  
x = orbits[0,:,ntest]*rscale
y = orbits[1,:,ntest]*rscale
z = orbits[2,:,ntest]*rscale
jr = actions[0,:]*rscale*vscale
jp = actions[1,:]*rscale*vscale
jz = actions[2,:]*rscale*vscale
r = orbitc[0,:,ntest]*rscale

simnamei = 'NoBar'
iterationi = str(0)
orbitsi = np.load('../orbits/'+simnamei+'/10000N_qiDF_MW14p_stklAA_orbits_cart_'+simnamei+iterationi+'.npy')  
orbitci = np.load('../orbits/'+simnamei+'/10000N_qiDF_MW14p_stklAA_orbits_cyl_'+simnamei+iterationi+'.npy')  
actionsi = np.load('../orbits/'+simnamei+'/10000N_qiDF_MW14p_stklAA_actions_'+simnamei+iterationi+'.npy')  
xi = orbitsi[0,:,ntest]*rscale
yi = orbitsi[1,:,ntest]*rscale
zi = orbitsi[2,:,ntest]*rscale
jri = actionsi[0,:]*rscale*vscale
jpi = actionsi[1,:]*rscale*vscale
jzi = actionsi[2,:]*rscale*vscale
ri = orbitci[0,:,ntest]*rscale