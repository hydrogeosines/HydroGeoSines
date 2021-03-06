# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:07:46 2020

@author: Daniel
"""
import pandas as pd
import numpy as np
import re

VALID_TYPE = {"ET", "BP", "GW"}

const = {}
# pressure conversion constants
const['_pucf'] = {'m': 1, 'dm': 0.1, 'cm': 0.01, 'mm': 0.001, 'pa': 0.00010197442889221, 'hpa': 0.010197442889221, 'kpa': 0.10197442889221, \
         'mbar': 0.010197442889221, 'bar': 10.197442889221, 'mmhg': 0.013595475598539, 'psi': 0.70308890742557, 'ft': 1200/3937, 'yd': 3600/3937, 'inch': 0.0254}

    
def import_csv(filepath,input_type: str, utc_offset: int, unit: str = "m", method: str ="add", check_duplicates=False): #, dt_fmt='excel', bp_col='baro'
    VALID_TYPE = {"ET", "BP", "GW"}
    #TODO: add header=True and location as keywords to enable a more fleixble location naming 
    
    if input_type not in VALID_TYPE:
        raise ValueError("data input type must be one of %r." % VALID_TYPE)
        
    # load the csv file into variable
    data = pd.read_csv(filepath,parse_dates=[0], infer_datetime_format=True)
        
    # make sure the first column is a correctly identified datetime    
    if data.dtypes[0] == "datetime64[ns]":
        data.rename(columns={data.columns[0]:"datetime"}, inplace = True)
        dt_col      = data.columns[0]
        val_cols    = data.columns[1::].values        
    else:    
        raise Exception("Error: First column must be a datetime column")  
    
    data = pd.melt(data,id_vars=[dt_col], var_name = "location") 
    data.insert(1,"dtype", input_type)
    
    #unit conversion always to meters    
    if unit.lower() in const['_pucf']: #case insensitive unit search
        pconv = const['_pucf'][unit.lower()]            
    else:
        raise ValueError("Error: The unit '" + unit + "' is unknown.")

    data["value"] = data.value*pconv
    data["unit"] = str("m") # always set to SI unit meter
    
    # sort the data in a standard way for easier identification of duplicates
    data.sort_values(by=["location", "dtype","datetime"], inplace = True)
    
    if method == "add":
        try:    
            data = data.append(data)
        except AttributeError:
            data = Data(columns=["datetime","dtype","location","value","unit"])
            data = data.append(data)
            
        data.sort_values(by=["location", "dtype","datetime"], inplace = True)
        data.reset_index(inplace=True, drop=True)
        print("New data was added...")
    #TODO: Implement other methods    
    else:     
        data = data   
        
    if check_duplicates == True:                       
        data.check_duplicates()
    
    return data    
      

#%%      
test = import_csv('test_data/fowlers_gap/acworth_short_baro.csv', input_type= "ET", utc_offset = 10) #, dt_fmt='%d/%m/%Y %H:%M'
#%%
#test['datetime'] = pd.to_datetime(test['datetime'],dayfirst=True)
pivot = test.pivot_table(index="datetime", columns=["dtype","location"], values="value")
