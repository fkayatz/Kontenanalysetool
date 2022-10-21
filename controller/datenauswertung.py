# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 10:53:20 2022

@author: Fabian Kayatz
"""

import pandas as pd
import numpy as np

def summieren_pro_kategorie_zeitintervall(df,zeitspalte,zeitintervall, kategoriespalte):
    list_kategorien=list(pd.unique(df[kategoriespalte].values.ravel()))
    df_zeiteinheit_index=df.groupby(
        pd.Grouper(key=zeitspalte, freq=zeitintervall)).sum().index
    df_zeiteinheit=pd.DataFrame(index=df_zeiteinheit_index)
    
    for kategorie in list_kategorien:
        df_zeiteinheit[kategorie]=df[df[kategoriespalte]==kategorie].groupby(
            pd.Grouper(key=zeitspalte, freq=zeitintervall))['Betrag'].sum()
    
    #Ersetzen aller Wert mit nan durch 0
    df_zeiteinheit.replace(np.nan,0,True)
    
    return(df_zeiteinheit)

def summieren_pro_hauptkategorie_zeitintervall(df, hauptkategorien):
    
    df_hauptkategorie_zeiteinheit=df[hauptkategorien].sum(axis=1)

    #Ersetzen aller Wert mit nan durch 0
    df_hauptkategorie_zeiteinheit.replace(np.nan,0,True)

    return(df_hauptkategorie_zeiteinheit)


def erstellen_auswertung_pro_zeitintervall(df_einzahlung_kategorien, df_auszahlung_kategorien, zeitintervall):
    
    df_auswertung_pro_zeitintervall=pd.DataFrame(columns=['Einzahlungen', 
                                                  'Auszahlungen', 
                                                  'Einnahmen', 
                                                  'Ausgaben',
                                                  'Sparen',
                                                  'Rücklagen',
                                                  'Ausgaben + Sparen',
                                                  'Ausgaben + Sparen + Rücklagen',
                                                  'Gewinn & Verlust',
                                                  'Gewinn & Verlust inkl. Rücklagen',
                                                  'Sparquote'
                                                  ]
                                         )
    
    dict_auswertungskategorien={'Einzahlungen':['Gehalt', 'staatl. Zuschüsse', 'Steuern', 'Bonusprogramme', 'sonstige Einzahlungen'],
                                'Auszahlungen':['Sparen', 'Rücklagen', 'Rückzahlungen', 'Konsum'], 
                                'Einnahmen':['Gehalt', 'staatl. Zuschüsse', 'Steuern', 'Bonusprogramme'],
                                'Ausgaben':['Konsum'], 
                                'Rücklagen':['Rücklagen'], #hier fehlt noch das Wertpapier
                                'Sparen':['Sparen']
                                }
    
    #Zusammenfassen der Hauptkategorien entsprechend der Auswertekategorien
    for kategorie in dict_auswertungskategorien:
        
        #Erstellen des DataFrames und Sortierung nach Hauptkategorien sowie Zuordnung df_einzahlung & df_auszahlung
        if kategorie in ['Einzahlungen', 'Einnahmen']:
            df=summieren_pro_kategorie_zeitintervall(df_einzahlung_kategorien, 'Buchung', zeitintervall, 'Hauptkategorie') 
        else:
            df=summieren_pro_kategorie_zeitintervall(df_auszahlung_kategorien, 'Buchung', zeitintervall, 'Hauptkategorie')  
        
        #Summieren der Hauptkategorien entsprechend der Auswertekategorien
        df_auswertung_pro_zeitintervall[kategorie]=summieren_pro_hauptkategorie_zeitintervall(df, dict_auswertungskategorien[kategorie])
    
    #Berechnung der Kennwerte Ausgaben + Sparen, Ausgaben + Sparen + Rücklagen, Gewinn&Verlust, Gewinn&Verlust inkl. Rücklagen, Sparquote
    df_auswertung_pro_zeitintervall['Ausgaben + Sparen']=df_auswertung_pro_zeitintervall[['Ausgaben', 'Sparen']].sum(axis=1)
    df_auswertung_pro_zeitintervall['Ausgaben + Sparen + Rücklagen']=df_auswertung_pro_zeitintervall[['Ausgaben', 'Sparen', 'Rücklagen']].sum(axis=1)
    df_auswertung_pro_zeitintervall['Gewinn & Verlust']=df_auswertung_pro_zeitintervall[['Einnahmen', 'Ausgaben', 'Sparen']].sum(axis=1)
    df_auswertung_pro_zeitintervall['Gewinn & Verlust inkl. Rücklagen']=df_auswertung_pro_zeitintervall[['Einnahmen', 'Ausgaben', 'Rücklagen', 'Sparen']].sum(axis=1)
    df_auswertung_pro_zeitintervall['Sparquote']=abs(df_auswertung_pro_zeitintervall['Sparen']/df_auswertung_pro_zeitintervall['Einnahmen'])
    
    return(df_auswertung_pro_zeitintervall)


def mittelwert_ueber_zeitraum(df, zeitraum, min_zeitraum, verhaeltnis = False, quotient_spalte = np.nan, zaehler_spalte=np.nan, nenner_spalte=np.nan):
    
    #Berechnung des Mittelwertes über einen bestimmten Zeitraum
    df_mittelwert_ueber_zeitraum=pd.DataFrame(columns=df.columns)
    
    if verhaeltnis == True:
        df_mittelwert_ueber_zeitraum=df[df.columns.difference([quotient_spalte])].rolling(zeitraum,min_zeitraum).mean()
    
        #Berechnung der Sparquote, vorherige Funktion darauf nicht anwendbar
        df_mittelwert_ueber_zeitraum[quotient_spalte]=abs(df_mittelwert_ueber_zeitraum[zaehler_spalte]/df_mittelwert_ueber_zeitraum[nenner_spalte])
    
    else:
        df_mittelwert_ueber_zeitraum=df.rolling(zeitraum,min_zeitraum).mean()
        
    return(df_mittelwert_ueber_zeitraum)

def stabw_ueber_zeitraum(df, zeitraum, min_zeitraum):
    
    #Berechnung des Standardabweichung über einen bestimmten Zeitraum
    df_stabw_ueber_zeitraum=pd.DataFrame(columns=df.columns)
    df_stabw_ueber_zeitraum=df.rolling(zeitraum,min_zeitraum).std(skipna=True, ddof=0)
    
    return(df_stabw_ueber_zeitraum)