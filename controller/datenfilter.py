# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 20:39:13 2022

@author: Fabian Kayatz
"""

import numpy as np

def  filter_positiv (daten, spalte, vergleichselement):
    #Durchsuchen des Dataframes nach Werten größer gleich 0
    list_filter=daten[spalte]>=0
    
    #Erstellen des Dataframes entsprechend des Filters
    df_filter=daten[list_filter == vergleichselement]
    
    return(df_filter)

def sortieren_in_kategorien(df):
    dict_kategorie={'Sparen':'spar',
                    'Notgroschen':'notgroschen',
                    'Wertpapier': 'wp-rechnung|isin',
                    'Reisen': 'reisen|urlaub',
                    'Spenden': 'spend|hilfe',
                    }

    for kategorie in dict_kategorie:
        filter_kategorie=df['Verwendungszweck'].str.contains(dict_kategorie[kategorie], case=False, na=False)
        df.loc[filter_kategorie,'Kategorie']=kategorie
    
    df['Kategorie'].replace([np.nan],'Konsum', inplace=True)
    
    return(df)

def sortieren_in_konsumkategorien(df):
    dict_kategorie={'Lebensmittel':'kaufland|konsum|frida|lidl|aldi|netto|edeka|penny|rewe|simmel|lebensmittelhandel|restaurant|nordsee gmbh|mcdonalds|burger king|dominos|baeck|backerei|backhaus|menu|sodexo|kochloeffel',
                    'Mobilität':'tankstelle|esso|star|tamoil|orlen|aral|total service station|Kraftfahrzeug|kfz|reifen|autohaus|parking|garage|parkhaus|bike|fahrrad|db vertrieb|handyticket',
                    'Kleidung & Schuhe':'esprit|h+m|s.oliver|sport scheck|peek & cloppenburg|ernstings fam|zalando|jack&jones|textilhandel|reno|deichmann',
                    'Drogerie':'dm|rossmann|muller 7 gmbh|drogerie',
                    'Telekommunikation':'vodafone|klarmobil',
                    'Versicherungen':'huk|alte leipziger leben|ergo|allianz',
                    'Gesundheit':'apotheke|gesundheit',
                    'Freizeit':'buchhandlung|buecher|lesen|kino|therme|schwimmbad|sport|globetrotter|decathlon|outdoor',
                    'Paypal':'paypal',#keine sinnvollen Kategorie
                    'Bargeldauszahlung':'bargeldauszahlung' #keine sinnvolle Kategorie
                    }
    
    for kategorie in dict_kategorie:
        filter_kategorie=df.index.str.contains(dict_kategorie[kategorie], case=False)
        value_kategorie=df[filter_kategorie].sum()
        
        df.drop(index=df[filter_kategorie].index, axis=0, inplace=True)
        df.loc[kategorie]=value_kategorie
        
    df.sort_values(ascending=True, inplace=True)
    
    return(df)
    