###############################################################################
#   TSolidBodyRotationWrapperPotential.py: Wrapper to make a potential rotate
#                                         with a time dependent pattern speed, around
#                                         the z axis
###############################################################################
from galpy.potential.WrapperPotential import parentWrapperPotential
from galpy.util import conversion
#from .WrapperPotential import parentWrapperPotential
#from ..util import conversion
class TSolidBodyRotationWrapperPotential(parentWrapperPotential):
    """Potential wrapper class that implements steadily changing solid-body rotation around the z-axis. 
    Can be used to make a bar or other perturbation change rotation rate. 
    The potential is rotated by replacing 

    .. math::
        \\phi \\rightarrow \\phi + \\Omega(t) \\times t + \\mathrm{pa}

    with 
    
    :math:`\\Omega` is steady at \\mathrm{omegai} when t < to 
    and
    :math:'\\Omega' steadily decreases to \\mathrm{omegaf} after t >= to
    and 
    :math:`\\mathrm{pa}` the position angle at :math:`t=0`.
    """
    def __init__(self,amp=1.,pot=None,omegai=1.,omegaf=1.,to=0.,tsteady=0.,pa=0.,ro=None,vo=None):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a TSolidBodyRotationWrapper Potential

        INPUT:

           amp - amplitude to be applied to the potential (default: 1.)

           pot - Potential instance or list thereof; this potential is made to rotate around the z axis by the wrapper

           omegai = (1.) the initial pattern speed (can be a Quantity)

           omegaf = (1.) the final pattern speed (can be a Quantity)
           
           to = (0.) time when pattern begins to slow (can be a Quantity)
           
           tsteady - time when the pattern speed stops slowing (can be a Quantity)

           pa = (0.) the position angle (can be a Quantity)
           
        OUTPUT:

           (none)

        HISTORY:

           2017-08-22 - SolidBodyRotationWrapper - Bovy (UofT)
           2021-07-07 - TSolidBodyRotationWrapper - Daniel (Bryn Mawr)

        """
        omegai= conversion.parse_frequency(omegai,ro=self._ro,vo=self._vo)
        omegaf= conversion.parse_frequency(omegaf,ro=self._ro,vo=self._vo)
        to= conversion.parse_time(to,ro=self._ro,vo=self._vo)
        tsteady= conversion.parse_time(tsteady,ro=self._ro,vo=self._vo)
        pa = conversion.parse_angle(pa)
        self._omegai= omegai
        self._omegaf= omegaf
        self._pa= pa
        self._to= to
        if tsteady is None:
            self._tsteady= 2*self._tform
        else:
            self._tsteady= tsteady
        self.hasC= False
        self.hasC_dxdv= False

#     def OmegaP(self):
#         """
#         NAME:
#            OmegaP
#         PURPOSE:
#            return the pattern speed
#         INPUT:
#            (none)
#         OUTPUT:
#            pattern speed
#         HISTORY:
#            2016-11-02 - Written - Bovy (UofT)
#         """
#         return self._omegat
    
    def _omegat(self,t):
        #Calculate relevant time
        if t < self._to:
            omegat= self._omegai
        elif t < self._tsteady:
            dO = self._omegaf-self._omegai
            dt = self._tsteady-self._to
            omegat= dO/dt *(t-self._to) + self._omegai
        else:
            omegat= self._omegaf
        return omegat 


    def _wrap(self,attribute,*args,**kwargs):
        kwargs['phi']= \
            kwargs.get('phi',0.)-self._omegat(kwargs.get('t',0.))*kwargs.get('t',0.)-self._pa
        return self._wrap_pot_func(attribute)(self._pot,*args,**kwargs)

# ###############################################################################
# #   TSolidBodyRotationWrapperPotential.py: Wrapper to make a potential rotate
# #                                         with a time dependent pattern speed, around
# #                                         the z axis
# ###############################################################################
# from galpy.potential.WrapperPotential import parentWrapperPotential
# from galpy.potential.Potential import _APY_LOADED
# from galpy.util import conversion
# if _APY_LOADED:
#     from astropy import units
# class TSolidBodyRotationWrapperPotential(parentWrapperPotential):
#     """Potential wrapper class that implements steadily changing solid-body rotation around the z-axis. 
#     Can be used to make a bar or other perturbation change rotation rate. 
#     The potential is rotated by replacing 

#     .. math::
#         \\phi \\rightarrow \\phi + \\Omega(t) \\times t + \\mathrm{pa}

#     with 
    
#     :math:`\\Omega` is steady at \\mathrm{omegai} when t < to 
#     and
#     :math:'\\Omega' steadily decreases to \\mathrm{omegaf} after t >= to
#     and 
#     :math:`\\mathrm{pa}` the position angle at :math:`t=0`.
#     """
#     def __init__(self,amp=1.,pot=None,omegai=1.,omegaf=1.,to=0.,tsteady=None,pa=0.,ro=None,vo=None):
#         """
#         NAME:

#            __init__

#         PURPOSE:

#            initialize a TSolidBodyRotationWrapper Potential

#         INPUT:

#            amp - amplitude to be applied to the potential (default: 1.)

#            pot - Potential instance or list thereof; this potential is made to rotate around the z axis by the wrapper

#            omegai = (1.) the initial pattern speed (can be a Quantity)

#            omegaf = (1.) the final pattern speed (can be a Quantity)
           
#            to = (0.) time when pattern begins to slow (can be a Quantity)
           
#            tsteady - time when the pattern speed stops slowing (can be a Quantity)

#            pa = (0.) the position angle (can be a Quantity)
           
#         OUTPUT:

#            (none)

#         HISTORY:

#            2017-08-22 - SolidBodyRotationWrapper - Bovy (UofT)
#            2021-07-07 - TSolidBodyRotationWrapper - Daniel (Bryn Mawr)

#         """
#         if _APY_LOADED and isinstance(omegai,units.Quantity):
#             omegai= omegai.to(units.km/units.s/units.kpc).value\
#                 /bovy_conversion.freq_in_kmskpc(self._vo,self._ro)
#         if _APY_LOADED and isinstance(omegaf,units.Quantity):
#             omegaf= omegaf.to(units.km/units.s/units.kpc).value\
#                 /bovy_conversion.freq_in_kmskpc(self._vo,self._ro)
#         if _APY_LOADED and isinstance(to,units.Quantity):
#             to= to.to(units.Gyr).value\
#                 /bovy_conversion.time_in_Gyr(self._vo,self._ro)
#         if _APY_LOADED and isinstance(tsteady,units.Quantity):
#             tsteady= tsteady.to(units.Gyr).value\
#                 /bovy_conversion.time_in_Gyr(self._vo,self._ro)
#         if _APY_LOADED and isinstance(pa,units.Quantity):
#             pa= pa.to(units.rad).value
#         self._omegai= omegai
#         self._omegaf= omegaf
#         self._pa= pa
#         self._to= to
#         if tsteady is None:
#             self._tsteady= 2*self._tform
#         else:
#             self._tsteady= tsteady
#         self.hasC= False
#         self.hasC_dxdv= False

#     def OmegaP(self):
#         """
#         NAME:
#            OmegaP
#         PURPOSE:
#            return the pattern speed
#         INPUT:
#            (none)
#         OUTPUT:
#            pattern speed
#         HISTORY:
#            2016-11-02 - Written - Bovy (UofT)
#         """
#         return self._omega
    
#     def _omegat(self,t):
#         #Calculate relevant time
#         if t < self._to:
#             omegat= omegai
#         elif t < self._tsteady:
#             dO = self._omegaf-self._omegai
#             dt = self._tsteady-self._to
#             omegat= dO/dt *(t-self._to) + omegai
#         else: #bar is fully on
#             omegat= omegaf
#         return omegat 

#     def _wrap(self,attribute,*args,**kwargs):
#         kwargs['phi']= \
#             kwargs.get('phi',0.)-self._omegat(kwargs.get('t',0.))*kwargs.get('t',0.)-self._pa
#         return self._wrap_pot_func(attribute)(self._pot,*args,**kwargs)

