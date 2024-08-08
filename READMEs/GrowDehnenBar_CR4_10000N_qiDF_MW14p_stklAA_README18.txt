Slowing Bar Integration

Made by Dr. Kate Daniel and Rowan Tolfree
-----------------------------------------
##### ADD A DESCRIPTION #####
-----------------------------------------

Created: 2024-08-01 18:49:04
Galpy 1.10.0

Set Parameters for Orbital Initial Conditions
	nsample : 1000                                     # number of samples per batch.
	nbatch :  10                                       # number of batches.
	norbit :  10000                                    # number of orbits.
	rmin :    0.0125                                   # sets scaled rmin.
	rmax :    1.25                                     # sets sclaed rmax.
	zmax :    0.3                                      # sets scales zmax.

Scales used for conversion from natural coordinates
	ro : 8.0                                      # (kpc) scale radi.
	vo : 220.0                                    # (km/s) scale velocity at ro.

Model parameters for potentials and DF:
	dpType : MW14                                     # Initial axi-symmetric potential for the disk
	AAType : stklAA                                   # Action Angle approx for ICs
	hro  : 0.33                                     # Scale length for surface density
	sro  : 0.16                                     # Radial velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)
	szo  : 0.08                                     # Vertical velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)
	hsro : 0.75                                     # Radial scale length for radial velocity dispersion profile
	hszo : 0.75                                     # Radial scale length for vertical velocity dispersion profile

### Set up the growing bar potential
# The bar potential was grown in GrowDenhenBar_CR4 simulation
# It completely formed over two bar periods and let equelibrate for 28 more. 

# Set up the bar potential
	rbo : 0.625                                    # Bar length is in natural units
	CRi : 0.5                                      # Initial corotation radius
	omegaBi : vc(CRi)/CRi : 2.025                                    # Pattern speed based on CR
	Ab : 1.0                                      # Bar strength (defaults to Ab=1)
	pa : 0.0                                      # Initial angle phi of the bar cc from x=0

bp_still = DehnenBarPotential(amp=Ab,a=ao,b=bo,c=co,omegab=omegaBi)

### Times relevant to integration ###

STEP 1: Find length of each timestep for adequate resolution

For adequate resolution, want timestep to be
	dtmaxPhys <0.75 Myr in physical units, which is equal to 
	dtmaxNat <0.0021 in natural units

Use these to define conversion factor:
	NatToGyrConversion = dtmaxPhys/dtmaxNat = 35.56 Myr per natural time unit

Slowing period for the bar is set to:
	TSlowPhys = 6.0 Gyr in physical units and
	TSlowNat = 168.75 in natural units

Therefore the total number of timesteps should be:
	Nsteps > TSlow/dtmax = ('8034.9', 1)

The number of steps is set to Nsteps = 8050
	where each step has length tstepPhys ~ 0.745 Myr in physical units
	and tstepNat ~ 0.02096 in natural time units

STEP 2: Identify timestamp for each rotation of the slowing bar

The array measuring time in natural units spaced by tstepNat is called tvector
	and has length len(tvector) = 8051

Inital pattern speed is omegaBi = 2.02 [natural units]
	As such a single bar period is: (using T = 2 pi / Omega_B)
	TbariNat = 3.1 natural units
	TbariPhys = 0.11 Gyr physical units
	Corotation at CRi = 4.0 kpc physical units

Final pattern speed is omegaBf = 0.83 [natural units]
	As such a single bar period is:
	TbarfNat = 7.603 natural units
	TbarfPhys = 0.27 Gyr physical units
	Corotation at CRf = 9.5 kpc physical units

The bar pattern speed is defined as:
	omegat = [(omegaBf - omegaBi) / TSlow] x (t-t0) + omegaBi
	where t0 is the initial time

The array with length 8051 giving the time dependent pattern speed is named omegat

The angle of the bar pattern over time:
	phit = omegat x (t-t0) + omegaBi x to
	where phit is implicitly in units of radians

The array with length 8051 giving the time dependent angle of the bar is named phit

In order to take snapshot when the bar is aligned with x=0
	must find the timestamp when phi=0 for each rotation.

Since phi(to)=0, cos(pho(to)=1)
	the local maxima in function cos(phit) will closely approximate x=0 for snapshots.

The array called maxpoints gives the indices of the 8050 maxima in cos(phit).
	This implies that the bar makes 8050 full rotations in 6.0 Gyr

