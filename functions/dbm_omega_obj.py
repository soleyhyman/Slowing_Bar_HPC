from imports import u, vcirc,DehnenBarPotential, MWPotential2014

class dbm_omega_obj:
    def __init__(self,rbo=0.625,Ab=1.0,pa=0.0,to=0.0,CRi=0.8,CRf=1.9,mwp=MWPotential2014,TSlow_num=6.0):
        # Set up the bar potential
        self.__rbo=rbo  # Bar length is in natural units (set to 5 kpc - Li+2016 at 6.7 kpc for same vo)
        self.__Ab=Ab    # Bar strength (defaults to Ab=1)
        self.__pa=pa    # The position angle of the x axis (radians)

        # Initialize slowing bar parameters 
        # Use ICs from time bar completely formed (set to be at 'to')
        self.__to=to               # Start time for simulation of a slowing bar [natural units]
        self.__CRi=CRi*self.__rbo  # Corotation radius [0.8xrbo=4kpc, 1.2xrbo=6kpc, 1.6xrbo=8kpc]
        self.__CRf=CRf*self.__rbo  # Corotation radius [0.8xrbo=4kpc, 1.2xrbo=6kpc, 1.6xrbo=8kpc]

        # from DiskModel
        self.__mwp=mwp  # initial axi-symmetric potential
        
        # to be calculated on initialization 
        self.__omegaBi=self.init_calc_omegaBi()      # Pattern speed based on CR
        self.__omegaBf=self.init_calc_omegaBf()      # Pattern speed based on CR
        self.__TSlowPhys=self.init_calc_TSlowPhys(TSlow_num)  # Total time for slowing bar [physical units]
        self.__bp_still=self.init_calc_bp_still()    # shape of the still dehnen bar potential
        
        # dictionary to store all params
        self.__params = {
            'rbo': self.__rbo,
            'Ab': self.__Ab,
            'pa': self.__pa,
            'to': self.__to,
            'CRi': self.__CRi,
            'CRf': self.__CRf,
            'mwp': self.__mwp,
            'omegaBi': self.__omegaBi,
            'omegaBf': self.__omegaBf,
            'TSlowPhys':self.__TSlowPhys,
            'bp_still': self.__bp_still
        }

    # math functions for obj initialization 
    def init_calc_omegaBi(self):
        return vcirc(self.__mwp,self.__CRi)/self.__CRi
    
    def init_calc_omegaBf(self):
        return vcirc(self.__mwp,self.__CRf)/self.__CRf 
    
    def init_calc_TSlowPhys(self,tslow_num):
        return  tslow_num*u.Gyr 
    
    def init_calc_bp_still(self):
        return DehnenBarPotential(
            amp = self.__Ab,
            omegab = None,
            rb = self.__rbo,
            barphi = self.__pa,
            Af = self.__Ab,
            tform = 0,
            tsteady = 0) 
    
    # static method to return input types
    @staticmethod
    def info():
        return 'Input vars in order:\n\trbo, Ab, pa, to, CRi(without rbo), CR(without rbo)f, mwp, TSlow_num'

    # getters
    def get_params(self):
        # Return an immutable dictionary of attributes
        return self.__params.copy()


