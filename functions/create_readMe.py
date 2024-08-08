###############diskmodel readme###########
# Setup simulation README
from imports import json,np,u,vcirc


def diskmodel_readme(json_path):
    #Creates the readme needed for diskmodel portion

    # open json and get sim data and readme path
    with open(json_path,'r') as json_file:
        data=json.load(json_file)
        sim_params= data['sim_params']
        readme_path=data['dir_data']['rmfile_dir']
        diskmodel_data=data['diskmodel_data']

    # make diskmodel Readme
    with open(readme_path,'a') as rm:
        rm.write('Set Parameters for Orbital Initial Conditions\n')
        rm.write(f"\tnsample : {str(sim_params['nstars']):<{40}} # number of samples per batch.\n")
        rm.write(f"\tnbatch :  {str(sim_params['nbatch']):<{40}} # number of batches.\n")
        rm.write(f"\tnorbit :  {str(sim_params['norbits']):<{40}} # number of orbits.\n")
        rm.write(f"\trmin :    {str(sim_params['rmin']):<{40}} # sets scaled rmin.\n")
        rm.write(f"\trmax :    {str(sim_params['rmax']):<{40}} # sets sclaed rmax.\n")
        rm.write(f"\tzmax :    {str(sim_params['zmax']):<{40}} # sets scales zmax.\n")
        rm.write('\n')

        rm.write('Scales used for conversion from natural coordinates\n')
        rm.write(f"\tro : {diskmodel_data['ro']:<{40}} # (kpc) scale radi.\n")
        rm.write(f"\tvo : {diskmodel_data['vo']:<{40}} # (km/s) scale velocity at ro.\n")
        rm.write('\n')

        rm.write('Model parameters for potentials and DF:\n')
        rm.write(f"\tdpType : {diskmodel_data['dpType']:<{40}} # Initial axi-symmetric potential for the disk\n")
        rm.write(f"\tAAType : {diskmodel_data['AAType']:<{40}} # Action Angle approx for ICs\n")

        rm.write(f"\thro  : {np.round(float(diskmodel_data['hro']),2):<{40}} # Scale length for surface density\n")
        rm.write(f"\tsro  : {diskmodel_data['sro']:<{40}} # Radial velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)\n")
        rm.write(f"\tszo  : {diskmodel_data['szo']:<{40}} # Vertical velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)\n")
        rm.write(f"\thsro : {diskmodel_data['hsro']:<{40}} # Radial scale length for radial velocity dispersion profile\n")
        rm.write(f"\thszo : {diskmodel_data['hszo']:<{40}} # Radial scale length for vertical velocity dispersion profile\n")
        rm.write('\n')

def dehnen_readme(json_path):
    # open json and get sim data and readme path
    with open(json_path,'r') as json_file:
        data=json.load(json_file)
        readme_path=data['dir_data']['rmfile_dir']
        dehnen_data=data['dehnenBarModel_Omega_data']

    # make diskmodel Readme
    with open(readme_path,'a') as rm:
        rm.write('### Set up the growing bar potential\n')
        rm.write('# The bar potential was grown in GrowDenhenBar_CR4 simulation\n')
        rm.write('# It completely formed over two bar periods and let equelibrate for 28 more. \n')
        rm.write('\n')

        rm.write("# Set up the bar potential\n")
        rm.write(f"\trbo : {dehnen_data['rbo']:<{40}} # Bar length is in natural units\n")
        rm.write(f"\tCRi : {dehnen_data['CRi']:<{40}} # Initial corotation radius\n")
        rm.write(f"\tomegaBi : vc(CRi)/CRi : {np.round(float(dehnen_data['omegaBi']),3):<{40}} # Pattern speed based on CR\n")
        rm.write(f"\tAb : {dehnen_data['Ab']:<{40}} # Bar strength (defaults to Ab=1)\n")
        rm.write(f"\tpa : {dehnen_data['pa']:<{40}} # Initial angle phi of the bar cc from x=0\n")
        rm.write('\n')
        rm.write('bp_still = DehnenBarPotential(amp=Ab,a=ao,b=bo,c=co,omegab=omegaBi)\n')
        rm.write('\n')

def TimeScaleCalc_readme(json_path):
    # open json and get sim data and readme path
    with open(json_path,'r') as json_file:
        data=json.load(json_file)
        readme_path=data['dir_data']['rmfile_dir']
        timeScaleVals=data['timeScaleVals_readme']
        dehnenBarModel_Omega_data=data['dehnenBarModel_Omega_data']
        diskmodel_data=data['diskmodel_data']

    # make TimeScaleCalc readme
    with open(readme_path,'a') as rm:
        rm.write("### Times relevant to integration ###\n")
        rm.write("\n")
        rm.write("STEP 1: Find length of each timestep for adequate resolution\n")
        rm.write("\n")

        rm.write("For adequate resolution, want timestep to be\n")
        rm.write(f"\tdtmaxPhys <{timeScaleVals['dtmaxPhys']} in physical units, which is equal to \n")
        rm.write(f"\tdtmaxNat <{timeScaleVals['dtmaxNat']} in natural units\n")
        rm.write("\n")

        rm.write("Use these to define conversion factor:\n")
        rm.write(f"\tNatToGyrConversion = dtmaxPhys/dtmaxNat = {timeScaleVals['NatToGyrConversion']} per natural time unit\n")
        rm.write("\n")

        rm.write("Slowing period for the bar is set to:\n")
        rm.write(f"\tTSlowPhys = {dehnenBarModel_Omega_data['TSlowPhys']} in physical units and\n")
        rm.write(f"\tTSlowNat = {timeScaleVals['TSlowNat']} in natural units\n")
        rm.write("\n")

        rm.write("Therefore the total number of timesteps should be:\n")
        rm.write(f"\tNsteps > TSlow/dtmax = {timeScaleVals['ntstepApprox'], 1}\n\n")
        rm.write(f"The number of steps is set to Nsteps = {timeScaleVals['Nsteps']}\n")
        rm.write(f"\twhere each step has length tstepPhys ~ {timeScaleVals['tstepPhys_c']} in physical units\n")
        rm.write(f"\tand tstepNat ~ {timeScaleVals['tstepNat']} in natural time units\n")
        rm.write("\n")

        rm.write("STEP 2: Identify timestamp for each rotation of the slowing bar\n")
        rm.write("\n")

        rm.write("The array measuring time in natural units spaced by tstepNat is called tvector\n")
        rm.write(f"\tand has length len(tvector) = {timeScaleVals['tvector_len']}\n")
        rm.write("\n")

        rm.write(f"Inital pattern speed is omegaBi = {np.round(float(dehnenBarModel_Omega_data['omegaBi']), 2)} [natural units]\n")
        rm.write(f"\tAs such a single bar period is: (using T = 2 pi / Omega_B)\n")
        rm.write(f"\tTbariNat = {timeScaleVals['TbariNat']} natural units\n")
        rm.write(f"\tTbariPhys = {timeScaleVals['TbariPhys']} physical units\n")
        rm.write(f"\tCorotation at CRi = {timeScaleVals['CRi_corot']} physical units\n\n")

        rm.write(f"Final pattern speed is omegaBf = {np.round(float(dehnenBarModel_Omega_data['omegaBf']), 2)} [natural units]\n")
        rm.write(f"\tAs such a single bar period is:\n")
        rm.write(f"\tTbarfNat = {timeScaleVals['TbarfNat']} natural units\n")
        rm.write(f"\tTbarfPhys = {timeScaleVals['TbarfPhys']} physical units\n")
        #fix
        rm.write(f"\tCorotation at CRf = {timeScaleVals['CRf_corot']} physical units\n")
        rm.write("\n")

        rm.write("The bar pattern speed is defined as:\n")
        rm.write("\tomegat = [(omegaBf - omegaBi) / TSlow] x (t-t0) + omegaBi\n")
        rm.write("\twhere t0 is the initial time\n")
        rm.write(f"\nThe array with length {timeScaleVals['len_omegat']} giving the time dependent pattern speed is named omegat\n\n")

        rm.write("The angle of the bar pattern over time:\n")
        rm.write("\tphit = omegat x (t-t0) + omegaBi x to\n")
        rm.write("\twhere phit is implicitly in units of radians\n\n")
        rm.write(f"The array with length {timeScaleVals['len_phit']} giving the time dependent angle of the bar is named phit\n")
        rm.write("\n")

        rm.write("In order to take snapshot when the bar is aligned with x=0\n")
        rm.write("\tmust find the timestamp when phi=0 for each rotation.\n")
        rm.write("\nSince phi(to)=0, cos(pho(to)=1)\n")
        rm.write("\tthe local maxima in function cos(phit) will closely approximate x=0 for snapshots.\n")
        rm.write(f"\nThe array called maxpoints gives the indices of the {timeScaleVals['len_phit'] - 1} maxima in cos(phit).\n")
        rm.write(f"\tThis implies that the bar makes {timeScaleVals['len_phit'] - 1} full rotations in {dehnenBarModel_Omega_data['TSlowPhys']}\n")
        rm.write("\n")

        # print('Important Note: The last index indicating x=0 is not the last step in the simulation,')
        # print('   rather it is at step i = ',maxpoints[0][-1],',')
        # print('   which is time',np.round(tvector[maxpoints[0][-1]],2),'in natural units and')
        # print('   and ',np.round((tvector[maxpoints[0][-1]]*NatToGyrConversion).to(u.Gyr),2),'in physical units.')
        # print('   This implies the final radius of corotation is R_CR=',np.round(endmwCR,2))

        # print('\n')

        # print('For reference, these maxima correspond to phi/(2 pi) = ',np.round(phit[maxpoints]/(2.*np.pi),4))

