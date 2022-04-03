# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 10:53:20 2022

@author: Fabian Kayatz
"""

import pandas as pd

def summieren_pro_kategorie_zeitintervall(df,zeitspalte,zeitintervall, kategoriespalte):
    list_kategorien=list(pd.unique(df[kategoriespalte].values.ravel()))
    df_zeiteinheit=pd.DataFrame()
    
    for kategorie in list_kategorien:
        df_zeiteinheit[kategorie]=df[df[kategoriespalte]==kategorie].groupby(
            pd.Grouper(key=zeitspalte, freq=zeitintervall))['Betrag'].sum()
        
    return(df_zeiteinheit)