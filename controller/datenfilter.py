# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 20:39:13 2022

@author: Fabian Kayatz
"""
def  filter_positiv (daten, spalte, vergleichselement):
    #Durchsuchen des Dataframes nach Werten größer gleich 0
    list_filter=daten[spalte]>=0
    
    #Erstellen des Dataframes entsprechend des Filters
    df_filter=daten[list_filter == vergleichselement]
    
    return(df_filter)
    