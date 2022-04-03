# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 20:39:13 2022

@author: Fabian Kayatz
"""

import numpy as np
import pandas as pd

def  filter_positiv (daten, spalte, vergleichselement):
    #Durchsuchen des Dataframes nach Werten größer gleich 0
    list_filter=daten[spalte]>=0
    
    #Erstellen des Dataframes entsprechend des Filters
    df_filter=daten[list_filter == vergleichselement]
    
    return(df_filter)



def sortieren_in_unterkategorien(df):
    #Deaktiviert den Fehler chained_assignment
    pd.options.mode.chained_assignment = None  # default='warn'
    
    dict_unterkategorien={'Nahrungsmittel, Getränke, Tabakwaren u.Ä.':('kaufland|konsum|frida|lidl|aldi|netto|edeka|penny'
                                                                       +'|rewe|simmel|lebensmittelhandel|restaurant'
                                                                       +'|nordsee gmbh|mcdonalds|burger king|dominos|'
                                                                       +'baeck|backerei|backhaus|menu|sodexo|kochloeffel|'
                                                                       +'essen|soup|fruehstueck|mittag|abendbrot|baguette'),
                          'Bekleidung und Schuhe':('esprit|h+m|s.oliver|sport scheck|peek & cloppenburg|ernstings fam|'
                                                   +'zalando|jack&jones|textilhandel|reno|deichmann|pull + bear|'
                                                   +'vivobaerfoot'),
                          'Wohnen, Energie, Wohnungsinstandhaltung':'wohnen|miete|strom|wasser|stadtwerke',
                          'Innenausstattung, Haushaltsgeräte und -gegenstände':'ikea|hoeffner|amzn|amazon|matraze|hausgeraet|karstadt|conrad',
                          'Gesundheit':'apotheke|gesundheit|friseur|haar|fielmann|apollo',
                          'Verkehr':'tankstelle|esso|star|tamoil|orlen|aral|total service station|Kraftfahrzeug|kfz|reifen|autohaus|parking|garage|parkhaus|bike|fahrrad|db vertrieb|handyticket|dvb',
                          'Post und Telekommunikation':'vodafone|klarmobil|vodafone|telekom',
                          'Freizeit, Unterhaltung und Kultur':'google|apple|buchhandlung|buecher|lesen|kino|therme|schwimmbad|sport|globetrotter|decathlon|outdoor|event|turn|fitbit|verlag',
                          'Bildungswesen':'schule|kindertageseinrichtung|kirchgemeinde dresden',
                          'Beherbungs- und Gaststättendienstleistungen':'restaurant|hotel|gaststätte|urlaub|ruestzeit|schenke|ferien',
                          'Versicherungen':'huk|alte leipziger leben|ergo|allianz',
                          'Spenden':'spend|hilfe',
                          'andere Waren und Dienstleistungen':'paypal|bargeldauszahlung|drogerie|blumen',
                          }

    dict_kontoinhaber = {'Kontoinhaber': 'Fabian Kayatz|Christina Kayatz|Familie Kayatz|Sophia Kayatz|Josua Kayatz|Naemi Kayatz|Kayatz|nan'
                         }
    
    dict_unterkonten = {'Sparen':'spar',
                        'Rücklage Notgroschen':'notgroschen',
                        'Wertpapier': 'wp-rechnung|isin|wertpapier',
                        'Rücklage Reisen': 'reisen|urlaub',
                        'Rückzahlungen': 'rueckzahlung|auslage|uebertrag|rueckueberweis|np.nan'
                         }
    
    #Kategorien für Ausgaben
    for kategorie in dict_unterkategorien:
        filter_kategorie=(df.loc[:,'Auftraggeber/Empfänger'].str.contains(dict_unterkategorien[kategorie], case=False, na=False)|
                          df.loc[:,'Verwendungszweck'].str.contains(dict_unterkategorien[kategorie], case=False, na=False)) 
        df.loc[filter_kategorie,'Unterkategorie']=kategorie
    
    #Kategorien für Überweisungen zwischen mehreren Konten der Kontoinhaber
    for kategorie in dict_unterkonten:
        filter_kategorie=(df.loc[:,'Verwendungszweck'].str.contains(dict_unterkonten[kategorie], case=False, na=False) & 
                          df.loc[:,'Auftraggeber/Empfänger'].str.contains(dict_kontoinhaber['Kontoinhaber'], case=True, na=False))
                         
        df.loc[filter_kategorie,'Unterkategorie']=kategorie
    
    #Prüfen ob Filter erfolgreich
    fehlermeldung='ACHTUNG: Die folgende Anzahl an Buchungen konnte keiner Unterkategorie zugeordnet werden:'
    if df['Unterkategorie'].isna().any()==True:
        print(fehlermeldung, df['Unterkategorie'].isna().sum())
    
    return(df)

def sortieren_in_hauptkategorien(df):
    #Deaktiviert den Fehler chained_assignment
    pd.options.mode.chained_assignment = None  # default='warn'
    
    
    dict_hauptkategorie={'Sparen':'Sparen',
                    'Rücklagen':'Rücklage Notgroschen|Rücklage Reisen',
                    'Wertpapier': 'Wertpapier',
                    'Rückzahlungen': 'Rückzahlungen',
                    'Konsum':('Nahrungsmittel, Getränke, Tabakwaren u.Ä.|'
                              +'Bekleidung und Schuhe|'
                              +'Wohnen, Energie, Wohnungsinstandhaltung|'
                              +'Innenausstattung, Haushaltsgeräte und -gegenstände|'
                              +'Gesundheit|'
                              +'Verkehr|'
                              +'Post und Telekommunikation|'
                              +'Freizeit, Unterhaltung und Kultur|'
                              +'Bildungswesen|'
                              +'Beherbungs- und Gaststättendienstleistungen|'
                              +'Versicherungen|'
                              +'Spenden|'
                              +'andere Waren und Dienstleistungen|'
                              +'unkategorisiert'
                              )
                    }

    for kategorie in dict_hauptkategorie:
        filter_kategorie=df.loc[:,'Unterkategorie'].str.contains(dict_hauptkategorie[kategorie], case=True, na=False)
        df.loc[filter_kategorie,'Hauptkategorie']=kategorie
    
    #Prüfen ob Filter erfolgreich
    fehlermeldung='ACHTUNG: Die folgende Anzahl an Buchungen konnte keiner Hauptkategorie zugeordnet werden:'
    if df['Hauptkategorie'].isna().any()==True:
        print(fehlermeldung, df['Hauptkategorie'].isna().sum())
    return(df)

def sortieren_in_kategorien(df):
    df=sortieren_in_unterkategorien(df)
    df.fillna('andere Waren und Dienstleistungen', inplace=True) #alternative 'unkategorisiert'
    df_auszahlung_kategorien=sortieren_in_hauptkategorien(df)
        
    return(df_auszahlung_kategorien)
    