# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:27:44 2022

@author: Fabian Kayatz
"""
import numpy as np
import pandas as pd

def unterkategorien_auswaehlen(gruppe):
    if gruppe == 'Einzahlungen':
        dict_unterkategorien={'Fraunhofer':('Fraunhofer'),
                              'FES':('landeskirche Sachsen'),
                              'Kindergeld':('Bundesagentur fur Arbeit'),
                              'Krankenkasse':('AOK'),
                              'Landeserziehungsgeld':('Hauptkasse des Freistaates Sachsen'),
                              'Steuern':('Finanzamt')
                              }
        
    if gruppe == 'Auszahlungen':
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
                              'Bildungswesen':'schule|kindertageseinrichtung|kirchgemeinde dresden|studentenbeitraege',
                              'Beherbungs- und Gaststättendienstleistungen':'restaurant|hotel|gaststätte|urlaub|ruestzeit|schenke|ferien',
                              'Versicherungen':'huk|alte leipziger leben|ergo|allianz',
                              'Spenden':'spend|hilfe',
                              'andere Waren und Dienstleistungen':'paypal|bargeldauszahlung|drogerie|blumen',
                              }
    return(dict_unterkategorien)

def hauptkategorien_auswaehlen(gruppe):
    if gruppe == 'Einzahlungen':
        dict_hauptkategorien={'Gehalt':('Fraunhofer|FES'),
                              'staatl. Zuschüsse':('Kindergeld|Elterngeld|Landeserziehungsgeld'),
                              'Steuern':('Steuern'),
                              'Bonusprogramme':('Krankenkasse'),
                              'sonstige Einzahlungen':('sonstige Einzahlungen')
                              }
        
    if gruppe == 'Auszahlungen':
        dict_hauptkategorien={'Sparen':'Sparen',
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
        
    return(dict_hauptkategorien)

def daten_unterkategorien_zuordnen(df, gruppe, dict_kontoinhaber,dict_unterkonten,dict_unterkategorien):   
    #Deaktiviert den Fehler chained_assignment
    pd.options.mode.chained_assignment = None  # default='warn'
      
    #Unterkategorien für Einnahmen/Ausgaben nicht vom Kontoinhaber
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
    fehlermeldung='ACHTUNG: Die folgende Anzahl an ' + gruppe + ' ' + 'konnte keiner Unterkategorie zugeordnet werden:'
    if df['Unterkategorie'].isna().any()==True:
        print(fehlermeldung, df['Unterkategorie'].isna().sum())
    
    if gruppe =='Einzahlungen':
        df['Unterkategorie'].fillna('sonstige Einzahlungen', inplace=True) #alternative 'unkategorisiert'
    if gruppe == 'Auszahlungen':
        df['Unterkategorie'].fillna('andere Waren und Dienstleistungen', inplace=True) #alternative 'unkategorisiert'
    return(df)

def daten_hauptkategorien_zuordnen(df,gruppe,dict_hauptkategorien):
    for kategorie in dict_hauptkategorien:
        filter_kategorie=df.loc[:,'Unterkategorie'].str.contains(dict_hauptkategorien[kategorie], case=True, na=False)
        df.loc[filter_kategorie,'Hauptkategorie']=kategorie
    
    #Prüfen ob Filter erfolgreich
    fehlermeldung='ACHTUNG: Die folgende Anzahl an' + ' ' + gruppe + ' ' + 'konnte keiner Hauptkategorie zugeordnet werden:'
    if df['Hauptkategorie'].isna().any()==True:
        print(fehlermeldung, df['Hauptkategorie'].isna().sum())
    
    return(df)

#Zuordnung der Einzahlung in Haupt- und Unterkategorien
def daten_kategorien_zuordnen(df):
    if (df['Betrag']>=0).all()==True:
        gruppe='Einzahlungen'
    if (df['Betrag']<=0).all()==True:
        gruppe='Auszahlungen'  
    
    #Laden der Dictionaries
    dict_kontoinhaber = {'Kontoinhaber': 'Fabian Kayatz|Christina Kayatz|Familie Kayatz|Sophia Kayatz|Josua Kayatz|Naemi Kayatz|Kayatz|nan'
                         }
        
    dict_unterkategorien=unterkategorien_auswaehlen(gruppe)  
    
    dict_unterkonten = {'Sparen':'spar',
                        'Rücklage Notgroschen':'notgroschen',
                        'Wertpapier': 'wp-rechnung|isin|wertpapier',
                        'Rücklage Reisen': 'reisen|urlaub',
                        'Rückzahlungen': 'rueckzahlung|auslage|uebertrag|rueckueberweis|np.nan'
                         }
    
    dict_hauptkategorien=hauptkategorien_auswaehlen(gruppe)
    
    #Zuordnen der Unterkategorien
    df=daten_unterkategorien_zuordnen(df,gruppe,dict_kontoinhaber,dict_unterkonten,dict_unterkategorien)

    #Zuordnen der Hauptkategorien
    df=daten_hauptkategorien_zuordnen(df,gruppe,dict_hauptkategorien)

    return(df)

