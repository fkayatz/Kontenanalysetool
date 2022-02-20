# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 13:44:25 2022

@author: Fabian Kayatz
"""
'''
Model       - Datenhaltung
View        - Präsentation / Darstellung / Benutzerinteraktion
Controller  - Logik / Aufbereitung / Bearbeitung
'''
import controller.datenimport as datenimport





if __name__ == '__main__':
    print(__name__)
    
    '''
    BENUTZEREINGABE
    '''
    #Ordnerpfad zu den Rohdaten vorgeben
    ordnerpfad = r'D:\Familie Kayatz\2 Finanzen\Girokonto\Kontenanalyse\Rohdaten'
    
    '''
    DATENIMPORT
    '''
    # df_rohdaten aus mehreren Dateien importieren und in einem DataFrame zusammenfügen
    list_dateien = datenimport.dateiliste_erstellen(ordnerpfad)
    list_dateipfade = datenimport.dateipfadliste_erstellen(ordnerpfad, list_dateien)
    df_rohdaten=datenimport.dataframe_erstellen(list_dateipfade)
    
    '''
    AUSGABE
    '''
    print(df_rohdaten)