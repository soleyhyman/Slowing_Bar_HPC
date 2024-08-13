from imports import u, np, argparse, json, vcirc, argrelextrema, lindbladR, np,os
from dir_func import get_unique_filename, json_serialize_full, get_short_filename
from svptfncts import loadData,saveData
from create_readMe import TimeScaleCalc_readme

TMaxDivFactor = 10 # Factor to divide circular orbital period at rmin
Nsteps = 8050 # Hard entered after COMMENTING OUT lines 49-50

# create parser
parser = argparse.ArgumentParser(description='Running TimeScaleCalc')
parser.add_argument('-rmd','--readmedir',type=str, nargs=1, help='Takes in the curr README dir')
parser.add_argument('-jd','--jsondir', type=str, nargs=1, help='Takes in the curr JSON dir') 
parser.add_argument('-sn', '--simname', type=str, nargs=1, help='The name of the output folder.')
args = vars(parser.parse_args())

# create inital funcitons to find length of each timestep for adequate resolution
def timescalePhys(R,vc): # <-- use R [kpc] and vc [km/s]
    R = R *u.kpc
    vc = vc *u.km/u.s
    T = 2 *np.pi *R/vc
    return T.to(u.Myr)

def timescaleNat(R,vc): # <-- use natural units
    T = 2 *np.pi *R/vc 
    return T

def findomegat(omegai, omegaf, t):
    dO = omegaf-omegai
    dt = t[-1]-t[0]
    omegat= dO/dt *(t-t[0]) + omegai
    return omegat 

def findphit(omegai, omegat, t):
    phit = omegat*t + omegai*t[0]
    return phit

# open json and take necissary data
with open(args['jsondir'][0],'r') as json_file:
    data=json.load(json_file)
    dir_data=data['dir_data']
    sim_params=data['sim_params']
    # load pickled objs
    diskmodel=loadData(data['dir_data']['dm_name'])
    dehnenBarModel_Omega=loadData(data['dir_data']['dbo_name'])
    # gets dicts of info
    diskmodel_data=diskmodel.get_params()
    dehnenBarModel_Omega_data=dehnenBarModel_Omega.get_params()

# set adiquite timestamps 
dtmaxPhys = timescalePhys(sim_params['rmin']*diskmodel_data['ro'],vcirc(diskmodel_data['mwp'],sim_params['rmin'],vo=diskmodel_data['vo'],ro=diskmodel_data['ro']))/TMaxDivFactor
dtmaxNat  = timescaleNat(sim_params['rmin'],vcirc(diskmodel_data['mwp'],sim_params['rmin']))/TMaxDivFactor

# Conversion factor
NatToGyrConversion = dtmaxPhys/dtmaxNat

# convert tslow
TSlowNat = ((dehnenBarModel_Omega_data['TSlowPhys']/NatToGyrConversion).decompose()).value

# pickles TSlowNat so it can be passed to integrate orbits
TSlowNat_name=get_short_filename('TSlowNat','pickle','./metadata/pickles')
saveData(TSlowNat,TSlowNat_name)
data['dir_data']['TSlowNat_dir']=TSlowNat_name

# determine aprox steps
ntstepApprox = ((dehnenBarModel_Omega_data['TSlowPhys']/dtmaxPhys).decompose()).value

# convert ##################
tstepPhys = dehnenBarModel_Omega_data['TSlowPhys']/Nsteps
tstepNat = ((tstepPhys/NatToGyrConversion).decompose()).value

## Find times for each slowing bar rotation
tvector = np.arange(dehnenBarModel_Omega_data['to'],TSlowNat,tstepNat)

# calc pattern speed
TbariNat = 2.*np.pi/dehnenBarModel_Omega_data['omegaBi']
TbarfNat = 2.*np.pi/dehnenBarModel_Omega_data['omegaBf']
TbariPhys = (TbariNat*NatToGyrConversion).to(u.Gyr)
TbarfPhys = (TbarfNat*NatToGyrConversion).to(u.Gyr)

# calc omegat
omegat = findomegat(dehnenBarModel_Omega_data['omegaBi'],dehnenBarModel_Omega_data['omegaBf'],tvector)

# calc phit
phit = findphit(dehnenBarModel_Omega_data['omegaBi'],omegat,tvector)

# use phit to find maxpoints for bar rotation
cosphit = np.cos(phit*u.rad)
maxpoints = argrelextrema(cosphit, np.greater)

endmwCR = lindbladR(diskmodel_data['mwp'],omegat[maxpoints[0][-1]],m='corotation')*diskmodel_data['ro']*u.kpc

####################################################################
# Setup meta data files

# tfile creation
tfile = f"{dir_data['sim_name_short']}_tvector"
tfile_unique = get_short_filename(tfile,'npy','./metadata')
np.save(tfile_unique,tvector)
data['dir_data']['tvector_dir']=tfile_unique

# tphiofile creation
tphiofile = f"{dir_data['sim_name_short']}_tphi0"
tphio_unique= get_short_filename(tphiofile,'npy','./metadata')
nphio = maxpoints[0]
nphio = np.insert(nphio,0,0)
np.save(tphio_unique,nphio)
data['dir_data']['tphio_dir']=tphio_unique

# create omeatfile download
omegatfile =  f"{dir_data['sim_name_short']}_Omegat"
omegat_unique = get_short_filename(omegatfile,'npy','./metadata')
np.save(omegat_unique,omegat[nphio])
data['dir_data']['omegat_dir']=omegat_unique

# values to save and pass to json
timeScaleVals_readme={
    'dtmaxPhys':np.round(dtmaxPhys, 2),
    'dtmaxNat':np.round(dtmaxNat/10,4),
    'NatToGyrConversion':np.round(NatToGyrConversion,2),
    'TSlowNat': np.round(TSlowNat,2),
    'ntstepApprox':np.round(ntstepApprox,1),
    'Nsteps': Nsteps,
    'tstepNat':np.round(tstepNat,5),
    'tvector_len':len(tvector),
    'TbariNat':np.round(TbariNat,2),
    'TbariPhys':np.round(TbariPhys,2),
    'TbarfNat':np.round(TbarfNat,3),
    'TbarfPhys': np.round(TbarfPhys,3),
    'len_omegat':len(omegat),
    'len_phit':len(phit),
    'tstepPhys_c':np.round(tstepPhys.to(u.Myr),3),
    'CRi_corot': np.round((TbariPhys * vcirc(diskmodel_data['mwp'], dehnenBarModel_Omega_data['CRi'], vo=diskmodel_data['vo'], ro=diskmodel_data['ro']) * u.km / u.s / (2. * np.pi)).to(u.kpc), 2),
    'CRf_corot':np.round((TbarfPhys * vcirc(diskmodel_data['mwp'], dehnenBarModel_Omega_data['CRf'], vo=diskmodel_data['vo'], ro=diskmodel_data['ro']) * u.km / u.s / (2. * np.pi)).to(u.kpc), 2)
}

# clean data for json
clean,dirty=json_serialize_full(timeScaleVals_readme)
data['timeScaleVals_readme']=clean

with open(args['jsondir'][0],'w') as json_file:
    json.dump(data,json_file,indent=4)
if int(os.environ["SLURM_ARRAY_TASK_ID"])==0:
    # create readme
    TimeScaleCalc_readme(args['jsondir'][0])

# write vars to be passed up to shell 
with open('metadata/dirs1.sh', 'w') as f:
    f.write(f"tvector_dir={tfile_unique}\n")
    f.write(f"tphio_dir={tphio_unique}\n")
    f.write(f"omegat_dir={omegat_unique}\n")