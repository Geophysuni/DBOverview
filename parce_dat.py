# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:33:24 2022

@author: zhuravlev.sd
"""

import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt


def import_csv():        
    field_investment_yearly = pd.read_csv('field_investment_yearly.csv')
    field_production_yearly = pd.read_csv('field_production_yearly.csv')
    field_reserves = pd.read_csv('field_reserves.csv')
    wellbore_development_all = pd.read_csv('wellbore_development_all.csv')
    wellbore_exploration_all = pd.read_csv('wellbore_exploration_all.csv')
    
    # lets create list of dicts, where we will store structed information
    
    name_list = list(field_reserves['fldName'])
    
    tmp_dat_list = []
    for name in name_list:
        tmp = {}
        tmp['Field'] = name.lower()
        tmp['IniOE'] = field_reserves[field_reserves['fldName'].str.lower()==tmp['Field']]['fldRecoverableOE'].values[0]
        tmp['PrYears'] = field_production_yearly[field_production_yearly['prfInformationCarrier'].str.lower()==
                                               tmp['Field']]['prfYear'].values
        tmp['Production'] = field_production_yearly[field_production_yearly['prfInformationCarrier'].str.lower()==
                                               tmp['Field']]['prfPrdOeNetMillSm3'].values
        tmp['ProductionWat'] = field_production_yearly[field_production_yearly['prfInformationCarrier'].str.lower()==
                                               tmp['Field']]['prfPrdProducedWaterInFieldMillSm3'].values
        
        tmp['InvYears'] = field_investment_yearly[field_investment_yearly['prfInformationCarrier'].str.lower()==
                                               tmp['Field']]['prfYear'].values
        tmp['Investment'] = field_investment_yearly[field_investment_yearly['prfInformationCarrier'].str.lower()==
                                               tmp['Field']]['prfInvestmentsMillNOK'].values
        
        # production wells
        tmp_years = wellbore_development_all[wellbore_development_all['wlbField'].str.lower()==tmp['Field']]['wlbCompletionYear'].values
        tmp_years_edited = tmp_years[tmp_years>0]
        tmp['PWYears'] = np.sort(np.unique(tmp_years_edited))
        nwells = np.zeros(len(tmp['PWYears']))
        for iy, y in enumerate(tmp['PWYears']):
            wlist = wellbore_development_all[(wellbore_development_all['wlbField'].str.lower()==tmp['Field']) & 
                                             (wellbore_development_all['wlbCompletionYear']==y)]
            nwells[iy] = len(wlist)
        tmp['PW'] = nwells
            
        # exploration wells
        tmp_years = wellbore_exploration_all[wellbore_exploration_all['wlbField'].str.lower()==tmp['Field']]['wlbCompletionYear'].values
        tmp_years_edited = tmp_years[tmp_years>0]
        tmp['EWYears'] = np.sort(np.unique(tmp_years_edited))
        nwells = np.zeros(len(tmp['EWYears']))
        for iy, y in enumerate(tmp['EWYears']):
            wlist = wellbore_exploration_all[(wellbore_exploration_all['wlbField'].str.lower()==tmp['Field']) & 
                                             (wellbore_exploration_all['wlbCompletionYear']==y)]
            nwells[iy] = len(wlist)
        
            
        tmp['EW'] = nwells
        tmp_dat_list.append(tmp)
        
    dat_list = []
    for el in tmp_dat_list:
        tmp = {}
        tmp['Field'] = el['Field']
        tmp['IniOE'] = el['IniOE']
        wholeYears = np.hstack((el['PrYears'], el['InvYears'], el['PWYears'] , el['EWYears']))
        tmp['Years'] = np.arange(np.min(wholeYears),np.max(wholeYears))
        tmp['Production'] = np.zeros(len(tmp['Years']))
        tmp['ProductionWat'] = np.zeros(len(tmp['Years']))
        tmp['Investment'] = np.zeros(len(tmp['Years']))
        tmp['PW'] = np.zeros(len(tmp['Years']))
        tmp['EW'] = np.zeros(len(tmp['Years']))
        
        tmp_PW = np.zeros(len(tmp['Years']))
        tmp_EW = np.zeros(len(tmp['Years']))
        
        for iy, y in enumerate(tmp['Years']):
            if len(np.where(el['PrYears']==y)[0])>0:
                tmp['Production'][iy] = el['Production'][np.where(el['PrYears']==y)]
            if len(np.where(el['PrYears']==y)[0])>0:
                tmp['ProductionWat'][iy] = el['ProductionWat'][np.where(el['PrYears']==y)]
            if len(np.where(el['InvYears']==y)[0])>0:
                tmp['Investment'][iy] = el['Investment'][np.where(el['InvYears']==y)]
            if len(np.where(el['PWYears']==y)[0])>0:
                tmp_PW[iy] = el['PW'][np.where(el['PWYears']==y)]
            if len(np.where(el['EWYears']==y)[0])>0:
                tmp_EW[iy] = el['EW'][np.where(el['EWYears']==y)]
        
        # tmp['PW'][0] = tmp_PW[0]
        # tmp['EW'][0] = tmp_EW[0]
        
        for i in range(len(tmp_PW)):
            tmp['PW'][i] = np.sum(tmp_PW[:i+1])
            tmp['EW'][i] = np.sum(tmp_EW[:i+1])
        
        tmp['Stage'] = np.zeros(len(tmp['Production']))
        tmp['UnitProd'] = np.zeros(len(tmp['Production']))
        
        for i in range(len(tmp['Production'])):
            tmp['UnitProd'][i] = 100*tmp['Production'][i]/tmp['IniOE']
            tmp['Stage'][i] = 100*np.sum(tmp['Production'][:i+1])/tmp['IniOE']
            
        tmp['ProductionWatPerc'] = 100*tmp['ProductionWat']/(tmp['ProductionWat']+tmp['Production'])
        
        dat_list.append(tmp)
    return dat_list
        

