Slowing Bar Integration

Made by Dr. Kate Daniel and Rowan Tolfree
-----------------------------------------
##### ADD A DESCRIPTION #####
-----------------------------------------

Created: 2024-08-01 18:22:52
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

