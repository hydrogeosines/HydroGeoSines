import hydrogeosines as hgs
import numpy as np
import pandas as pd
from copy import deepcopy

#%% Csiro Data
#%%  Testing MVC principal
acworth_site = hgs.Site('death valley', geoloc=[-116.471360, 36.408130, 688])
acworth_site.import_csv('tests/data/death_valley/Rau_et_al_2021.csv',
                        input_category=["GW","BP","ET"], utc_offset=0, unit=["m","m","nstr"],
                        how="add", check_duplicates=True)

#%% Processing
# create Instance of Processing with csiro_site
process_acworth = hgs.Processing(acworth_site)

# test hals method
hals_results  = process_acworth.hals()

# test hals method
fft_results  = process_acworth.fft(update=True)

#%% 
# test gw_correct
gw_correct_results  = process_acworth.GW_correct(lag_h=24, et_method = None, fqs=None)

#%%
# test be method
be_time  = process_acworth.BE_time(method="all", update=True)
print(be_time)

#%% frequency domain stuff ...

be_freq  = process_acworth.BE_freq(method="rau", freq_method='hals', update=True)
print(be_freq)
