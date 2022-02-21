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
from controller import datenimport
from controller import datenaufbereitung
from controller import datenfilter




if __name__ == '__main__':
    print(__name__)
    
    '''
    BENUTZEREINGABE
    Definition der Variablen und Eingabebefehle zukünftigt können auch HMIs hinzukommen.
    '''
    #Ordnerpfad zu den Rohdaten vorgeben
    ordnerpfad = r'D:\Familie Kayatz\2 Finanzen\Girokonto\Kontenanalyse\Rohdaten'
    
    '''
    DATENIMPORT
    1. Daten aus Excelfiles auslesen und in einem DataFrame zusammenfügen
    2. Aufbereitung der Rohdaten, z.B. Duplikate entfernen, Sortieren, Neuindexieren
    '''
    # df_rohdaten aus mehreren Dateien importieren und in einem DataFrame zusammenfügen
    list_dateien = datenimport.dateiliste_erstellen(ordnerpfad)
    list_dateipfade = datenimport.dateipfadliste_erstellen(ordnerpfad, list_dateien)
    df_rohdaten=datenimport.dataframe_erstellen(list_dateipfade)
    
    # df_rohdaten abspeichern als df_daten und aufbereiten der Daten (Duplikate entfernen, sortieren, neuindexieren)
    df_daten=df_rohdaten.copy()
    datenaufbereitung.duplikate_entfernen(df_daten, True)
    datenaufbereitung.daten_sortieren(df_daten, True, 'Buchung', False)
    datenaufbereitung.reset_index(df_daten, True)
    
    '''
    EINZAHLUNGEN UND AUSZAHLUNGEN AUF DAS KONTO
    1. Erstellung der DataFrames df_konto_einzahlungen und df_konto_auszahlungen
    2. Gruppieren der Dataframes nach dem Auftraggeber und Sortieren nach der Betragssumme
    '''
    #Erstellung von 2 Dataframes mit den Einzahlungen und Auszahlungen auf das Konto
    df_konto_einzahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', True)
    df_konto_auszahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', False)
    
    #Gruppieren der Datenframes Einzahlungen und Auszahlungen nach Auftraggeber und Sortieren nach der Betragssumme
    df_quelle_einzahlung=df_konto_einzahlungen['Betrag'].groupby(df_konto_einzahlungen['Auftraggeber/Empfänger']).sum().sort_values(ascending=False)
    df_quelle_auszahlung=df_konto_auszahlungen['Betrag'].groupby(df_konto_auszahlungen['Auftraggeber/Empfänger']).sum().sort_values(ascending=True)
    '''
    AUSGABE
    '''
    print(df_daten)