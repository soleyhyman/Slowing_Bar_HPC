from imports import MWPotential2014
class DiskModel_obj:
    def __init__(self,ro=8.0,vo=220.0,hro=1.0/3.0,sro=0.16,szo=0.08,hsro=0.75,hszo=0.75,
                 AAType='stklAA',dpType='MW14',mwp=MWPotential2014):
        self.__ro = ro         # (kpc) scale radii
        self.__vo = vo         # (km/s) scale velocity at ro
        self.__hro = hro       # Scale length for surface density
        self.__sro = sro       # Radial velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)
        self.__szo = szo       # Vertical velocity dispersion at ro in natural coordinates (times vo to get in physical at ro)
        self.__hsro = hsro     # Radial scale length for radial velocity dispersion profile
        self.__hszo = hszo     # Radial scale length for vertical velocity dispersion profile
        self.__AAType = AAType # Action Angle approx for ICs
        self.__dpType = dpType # Type of potential
        self.__mwp = mwp       # Underlying initial axi-symmetric potential

        # dictionary to store all parameters 
        self.__params = {
            'ro': self.__ro,
            'vo': self.__vo,
            'hro': self.__hro,
            'sro': self.__sro,
            'szo': self.__szo,
            'hsro': self.__hsro,
            'hszo': self.__hszo,
            'AAType': self.__AAType,
            'dpType': self.__dpType,
            'mwp': self.__mwp
        }

    # method to return the input info
    @staticmethod
    def info():
        return 'Input vars in order:\n\tro, vo, hro, sro, szo, hsro, hszo, AAType, dpType, mwp'

    # getters
    def get_params(self):
        # Return an immutable dictionary of attributes
        return self.__params.copy()