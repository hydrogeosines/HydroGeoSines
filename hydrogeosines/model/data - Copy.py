import numpy as np
import pandas as pd

# import sub-classes

from .time import Time
from .series import Series
from .read import Read

#%% the data handling class

class Data(pd.DataFrame,Time,Series,Read):
    
    # this makes it so our class returns an instance
    # of ExtendedDataFrame, instead of a regular DataFrame
    @property
    def _constructor(self):
        return Data

    @property
    def dtf(self):
        return self.dt_num(self.datetime)

    @property
    def dts(self):
        return self.dt_str(self.datetime)
    
    @property
    def dtf_utc(self):
        return self.dt_num(self.datetime, utc=True)
    
    @property
    def dts_utc(self):
        return self.dt_str(self.datetime, utc=True)

    @property
    def spd(self):
        return 86400/self.spl_period(self.datetime, unit='s')

#%% does not belong here and needs to be rewritten
    def is_regular(self, loc: str):
        tmp = self[self['location'] == loc]['datetime']
        tmp = np.diff(self.dt_num(tmp)*86400)
        idx = (tmp != tmp[0])
        if np.any(idx):
            return False
        else:
            return True
    

