# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:27:14 2022

@author: Fabian Kayatz
"""

def duplikate_entfernen(daten, duplikate_entfernen):
    if duplikate_entfernen == True:
        daten = daten.drop_duplicates(inplace=True)
    return(daten)

def daten_sortieren(daten, sortieren, spalten, absteigend):
    if sortieren == True:
        daten.sort_values(by=[spalten], inplace=True, ascending=absteigend)
    return(daten)
        
def reset_index(daten, reset_index):
    if reset_index == True:
        daten.reset_index(drop = True, inplace = True)
    return(daten)