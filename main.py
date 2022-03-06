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
from view import ploterzeugung


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
    3. Zusammenfassen ähnlicher Ausgabengruppen
    '''
    #Erstellung von 2 Dataframes mit den Einzahlungen und Auszahlungen auf das Konto
    df_konto_einzahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', True)
    df_konto_auszahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', False)
    
    #Erstellung von 2 DataFrames Einzahlung vom Kontoinhaber und Einzahlungen von sonstigen
    df_einzahlungen_von_inhaber=df_konto_einzahlungen[df_konto_einzahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=False)]
    df_einzahlungen_ohne_inhaber=df_konto_einzahlungen[df_konto_einzahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=False)==False]
    
    #Erstellung von 2 DataFrames Auszahlung vom Kontoinhaber und Auszahlungen von sonstigen
    df_auszahlungen_zu_inhaber=df_konto_auszahlungen[df_konto_auszahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=True)]
    df_auszahlungen_ohne_inhaber=df_konto_auszahlungen[df_konto_auszahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=True)==False]
    
    #Gruppieren der Datenframes Einzahlungen und Auszahlungen nach Auftraggeber und Sortieren nach der Betragssumme
    df_quelle_einzahlung=df_einzahlungen_ohne_inhaber['Betrag'].groupby(df_einzahlungen_ohne_inhaber['Auftraggeber/Empfänger']).sum().sort_values(ascending=False)
    df_quelle_auszahlung=df_auszahlungen_ohne_inhaber['Betrag'].groupby(df_auszahlungen_ohne_inhaber['Auftraggeber/Empfänger']).sum().sort_values(ascending=True) #hier sind noch die Kayatz enthalten
    
    #Zusammenfassen ähnlicher Gruppen
    datenfilter.sortieren_in_konsumkategorien(df_quelle_auszahlung)
    
    #Sortieren der Ausgaben in Kategorien    
    df_konto_grouped_auszahlungen=datenfilter.sortieren_in_kategorien(df_konto_auszahlungen)
    
    #Quelle ausgeben NUR VORÜBERGEHEND ALS ÜBERBLICK  
    df_quelle_auszahlung_all=df_konto_grouped_auszahlungen['Betrag'].groupby(df_konto_grouped_auszahlungen['Kategorie']).sum()
    
    
    '''
    AUSGABE
    1. Erstellen eines Sankey-Plots für Ein- und Auszahlungen
    '''
    #Sankey-Plot Ein- und Auszahlung ohne Kontoinhaber
    #ploterzeugung.create_sankey_plot(df_quelle_einzahlung, abs(df_quelle_auszahlung))
    
    #Datenausgabe
    print(df_daten)
