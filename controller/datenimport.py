# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:52:45 2022

@author: Fabian Kayatz
"""
import os
import pandas as pd

def dateiliste_erstellen(ordnerpfad):
    #Erstellung einer Liste mit im Ordnerpfad enthaltenen Dateien
    dateiliste = os.listdir(ordnerpfad)
    return(dateiliste)


def dateipfadliste_erstellen(ordnerpfad, dateiliste):
    #Es wird eine Liste erstellt, indem die Dateiliste mit dem Ordnerpfad kombiniert wird.
    def dateipfad_erstellen(datei):
        dateipfad = os.path.join(ordnerpfad, datei)
        return(dateipfad)
    dateipfadliste = list(set(map(dateipfad_erstellen, dateiliste)))
    return(dateipfadliste)


def dataframe_erstellen(dateipfadliste):
    # Ziel der Funktion ist es die Daten aus den einzelnen Datei in einem Dataframe zu bündeln.
    # Gibt es hier noch eine bessere Funktion?
    df = pd.DataFrame(columns=['Buchung',
                               'Valuta',
                               'Auftraggeber/Empfänger',
                               'Buchungstext',
                               'Verwendungszweck',
                               'Saldo',
                               'Währung',
                               'Betrag',
                               'Währung.1'
                               ]
                      )
    
    for i in dateipfadliste:

        df = df.append(pd.read_csv(i,
                                   parse_dates=[0, 1],
                                   dayfirst=True,
                                   delimiter=';',
                                   header=13,
                                   thousands='.',
                                   decimal=',',
                                   skip_blank_lines=False,
                                   encoding='latin1'
                                   )
                       )
     
    return(df)



