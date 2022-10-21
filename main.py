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
from controller import datenauswertung
from controller import datenkategorien
from controller import programm_monitoring
from controller import zeitmodul
from view import datenplots

'''
STARTZEIT
'''
hauptprogramm_monitoring=programm_monitoring.ProgrammLaufzeit('Hauptprogramm')
hauptprogramm_monitoring.startzeit_definieren()

if __name__ == '__main__':
    print(__name__)
    
    '''
    BENUTZEREINGABE
    Definition der Variablen und Eingabebefehle zukünftigt können auch HMIs hinzukommen.
    '''
    #Ordnerpfad zu den Rohdaten vorgeben
    kontoinhaber = 'Fabian Kayatz'
    ordnerpfad = r'D:\Familie Kayatz\2 Finanzen\Girokonto\Kontenanalyse\Rohdaten'
    datum_format='%d.%m.%y'
    
    '''
    DATENIMPORT
    1. Daten aus Excelfiles auslesen und in einem DataFrame zusammenfügen
    2. Aufbereitung der Rohdaten, z.B. Duplikate entfernen, Sortieren, Neuindexieren
    3. Füllen der Spalte Emfpänger im Fall "nan" mit dem Kontoinhaber
    4. Anpassen des Zeitformats (in Arbeit)
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
    
    #Empfänger = nan ersetzen durch Kontoinhaber
    df_daten.loc[df_daten['Auftraggeber/Empfänger'].isna(),'Auftraggeber/Empfänger']=kontoinhaber
    
    #Ändern des Datumformats
    #df_daten['Buchung']=df_daten['Buchung'].dt.strftime(datum_format) #führt zu einer Ausgabe als String
    
    
    '''
    EINZAHLUNGEN UND AUSZAHLUNGEN AUF DAS KONTO
    1. Erstellung der DataFrames df_konto_einzahlungen und df_konto_auszahlungen
    2. Zuordnung der Ein- und Auszahlungen in Haupt- und Unterkategorien
    3. Erstellung einer Ein- und Auszahlungsübersicht über Kategorie und Zeitintervall
    4. Erstellung eines DataFrames mit Auswertungen pro Zeitintervall
    5. Erstellung eines DateFrames welches den Mittelwert der Werte über einen Zeitraum bestimmt
    '''
    #Erstellung von 2 Dataframes mit den Einzahlungen und Auszahlungen auf das Konto
    df_konto_einzahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', True)
    df_konto_auszahlungen=datenfilter.filter_positiv(df_daten, 'Betrag', False)
    
    #Zuordnung der Einzahlung bzw. Auszahlungen in Haupt- und Unterkategorien
    df_einzahlung_kategorien=datenkategorien.daten_kategorien_zuordnen(df_konto_einzahlungen)
    df_auszahlung_kategorien=datenkategorien.daten_kategorien_zuordnen(df_konto_auszahlungen)
    #print(df_auszahlung_kategorien['Betrag'].groupby(df_auszahlung_kategorien['Unterkategorie']).sum().sort_values(ascending=True))
    
    #Erstellen eines DataFrames mit einer Einzahlungs- bzw. Auszahlungsübersicht über Unterkategorie und Monat
    df_einzahlung_pro_kategorie_monat = datenauswertung.summieren_pro_kategorie_zeitintervall(df_einzahlung_kategorien, 
                                                                                              'Buchung', 
                                                                                              'M', 
                                                                                              'Unterkategorie'
                                                                                              )
    
    df_auszahlung_pro_kategorie_monat = datenauswertung.summieren_pro_kategorie_zeitintervall(df_auszahlung_kategorien, 
                                                                                              'Buchung', 
                                                                                              'M', 
                                                                                              'Unterkategorie'
                                                                                              )
    
    #Erstellen eines DataFrames mit einer Auswertung über das Zeitintervall/Monat   
    df_auswertung_pro_monat=datenauswertung.erstellen_auswertung_pro_zeitintervall(df_einzahlung_kategorien, 
                                                                                   df_auszahlung_kategorien, 
                                                                                   'M'
                                                                                   )
    df_auswertung_pro_jahr=datenauswertung.erstellen_auswertung_pro_zeitintervall(df_einzahlung_kategorien, 
                                                                                  df_auszahlung_kategorien, 
                                                                                  'Y'
                                                                                  )
    
    #Berechnung der Mittelwertdaten der Hauptkategorien über die letzten Monate
    df_auswertung_pro_monat_mw12=datenauswertung.mittelwert_ueber_zeitraum(df_auswertung_pro_monat, 12, 3, True, 'Sparquote', 'Sparen', 'Einnahmen')
    
    #Berechnung der Standardabweichung der Hauptkategorien über die letzten Monate
    df_auswertung_pro_monat_stabw12=datenauswertung.stabw_ueber_zeitraum(df_auswertung_pro_monat, 12, 3)
    
    #Berechnung der Mittelwertdaten der Unterkategorien über die letzten Monate
    df_auszahlung_pro_kategorie_monat_mw12=datenauswertung.mittelwert_ueber_zeitraum(df_auszahlung_pro_kategorie_monat, 12, 3)
    
    #Berechnung der Standardabweichung der Unterkategorien über die letzten Monate
    df_auszahlung_pro_kategorie_monat_stabw12=datenauswertung.stabw_ueber_zeitraum(df_auszahlung_pro_kategorie_monat, 12, 3)
    '''
    #Erstellung von 2 DataFrames Einzahlung vom Kontoinhaber und Einzahlungen von sonstigen
    df_einzahlungen_von_inhaber=df_konto_einzahlungen[df_konto_einzahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=False)]
    df_einzahlungen_ohne_inhaber=df_konto_einzahlungen[df_konto_einzahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=False)==False]
    
    #Erstellung von 2 DataFrames Auszahlung vom Kontoinhaber und Auszahlungen von sonstigen
    df_auszahlungen_zu_inhaber=df_konto_auszahlungen[df_konto_auszahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=True)]
    df_auszahlungen_ohne_inhaber=df_konto_auszahlungen[df_konto_auszahlungen['Auftraggeber/Empfänger'].str.contains('Fabian Kayatz|Christina Kayatz|Familie Kayatz', case=False, na=True)==False]
    
    #Gruppieren der Datenframes Einzahlungen und Auszahlungen nach Auftraggeber und Sortieren nach der Betragssumme
    df_quelle_einzahlung=df_einzahlungen_ohne_inhaber['Betrag'].groupby(df_einzahlungen_ohne_inhaber['Auftraggeber/Empfänger']).sum().sort_values(ascending=False)
    df_quelle_auszahlung=df_auszahlungen_ohne_inhaber['Betrag'].groupby(df_auszahlungen_ohne_inhaber['Auftraggeber/Empfänger']).sum().sort_values(ascending=True) #hier sind noch die Kayatz enthalten
    
    
    #Verwendungszweck ausgeben
    df_quelle_auszahlung_all=df_auszahlung_kategorien['Betrag'].groupby(df_auszahlung_kategorien['Hauptkategorie']).sum()

    #Quelle ausgeben NUR VORÜBERGEHEND ALS ÜBERBLICK  
    df_quelle_auszahlung_all=df_auszahlung_kategorien['Betrag'].groupby(df_auszahlung_kategorien['Hauptkategorie']).sum()
    '''
    
    '''
    AUSGABE
    1. Erstellen eines Sankey-Plots für Ein- und Auszahlungen
    '''
    #Sankey-Plot Ein- und Auszahlung ohne Kontoinhaber
    #datenplots.create_sankey_plot(df_quelle_einzahlung, abs(df_quelle_auszahlung))
    
    #Datenausgabe
    #print(df_daten)
    
    #Diagramme
    #Saldo über die Zeit
    datenplots.liniendiagramm_erstellen(df_daten['Buchung'],
                                        df_daten[['Saldo']], 
                                        'Saldo', 
                                        'Kontosaldo in €', 
                                        'Datum'
                                        ) 
    
    #Einnahmen- und Ausgaben pro Monat
    datenplots.saeulendiagramm_erstellen(abs(df_auswertung_pro_monat[['Einnahmen','Ausgaben']]), 
                                         'Ein- und Ausgaben',
                                         'Wert in €'
                                         )
    
    #Gewinn & Verlust pro Monat mit/ohne Rücklagen
    datenplots.saeulendiagramm_erstellen(df_auswertung_pro_monat[['Gewinn & Verlust', 'Gewinn & Verlust inkl. Rücklagen']], 
                                         'Gewinn & Verlust', 
                                         'Wert in €'
                                         )
    
    #Gewinn & Verlust pro Jahr mit/ohne Rücklagen
    datenplots.saeulendiagramm_erstellen(df_auswertung_pro_jahr[['Gewinn & Verlust', 'Gewinn & Verlust inkl. Rücklagen']], 
                                         'Gewinn & Verlust', 
                                         'Wert in €'
                                         )   
    
    #Einnahmen pro Monat inkl. Mittelwert und StAbw über die letzten 12 Monate
    datenplots.saeulen_linien_diagramm_erstellen(df_auswertung_pro_monat.index, 
                                                 df_auswertung_pro_monat['Einnahmen'],
                                                 df_auswertung_pro_monat_mw12['Einnahmen'],
                                                 df_auswertung_pro_monat_stabw12['Einnahmen'],
                                                 'Einnahmen',
                                                 'Einnahmen in €'
                                                 )
    
    #Ausgaben pro Monat inkl. Mittelwert und StAbw über die letzten 12 Monate
    datenplots.saeulen_linien_diagramm_erstellen(df_auswertung_pro_monat.index, 
                                                 df_auswertung_pro_monat['Ausgaben'],
                                                 df_auswertung_pro_monat_mw12['Ausgaben'],
                                                 df_auswertung_pro_monat_stabw12['Ausgaben'],
                                                 'Ausgaben', 
                                                 'Ausgaben in €'
                                                 )
    
    #Sparquote pro Monat inkl. Mittelwert und StAbw über die letzten 12 Monate
    datenplots.saeulen_linien_diagramm_erstellen(df_auswertung_pro_monat.index, 
                                                 df_auswertung_pro_monat['Sparquote'],
                                                 df_auswertung_pro_monat_mw12['Sparquote'],
                                                 df_auswertung_pro_monat_stabw12['Sparquote'],
                                                 'Sparquote',
                                                 'Sparquote in [-]'
                                                 )
    
    #Auszahlungen im aktuellen Monat
    heutiges_datum=zeitmodul.heutiges_datum_bestimmen()
    letzter_tag_im_monat=zeitmodul.letzter_tag_im_monat_bestimmen(heutiges_datum)
    datenplots.saeulendiagramm_erstellen(df_auszahlung_pro_kategorie_monat.transpose()[[letzter_tag_im_monat.strftime('%Y-%m-%d')]], 
                                         'Auszahlungen aktueller Monat',
                                         'Auszahlungen in €'
                                         )
    
    #Mittlere Auszahlung der letzten 12 Monate (noch in der Entwicklung, Berechnung stimmt nicht da Monate mit nan ignoriert werden)
    heutiges_datum=zeitmodul.heutiges_datum_bestimmen()
    letzter_tag_im_monat=zeitmodul.letzter_tag_im_monat_bestimmen(heutiges_datum)
    datenplots.saeulendiagramm_erstellen(df_auszahlung_pro_kategorie_monat_mw12.transpose()[[letzter_tag_im_monat.strftime('%Y-%m-%d')]],
                                         'Auszahlung letzten 12 Monaten',
                                         'Auszahlung in €'
                                         )      
    
    #ENTWICKLUNGSBEREICH   
        
    #Übersicht Einnahmen und Auszahlungstypen
    import pandas as pd
    df_a = pd.DataFrame(columns=['Einnahmen','Ausgaben', 'Ausgaben + Sparen', 'Ausgaben + Sparen + Rücklagen'])
    df_a['Einnahmen']=df_auswertung_pro_monat['Einnahmen']
    df_a['Ausgaben']=abs(df_auswertung_pro_monat['Ausgaben'])
    df_a['Ausgaben + Sparen']=abs(df_auswertung_pro_monat['Ausgaben']+df_auswertung_pro_monat['Sparen'])
    df_a['Ausgaben + Sparen + Rücklagen']=abs(df_auswertung_pro_monat['Ausgaben']+df_auswertung_pro_monat['Sparen']+df_auswertung_pro_monat['Rücklagen'])

    datenplots.liniendiagramm_mit_fuellbereich_erstellen(df_a.index, df_a[['Einnahmen']], df_a[['Ausgaben', 'Ausgaben + Sparen', 'Ausgaben + Sparen + Rücklagen']], 'Übersicht', 'Betrag in €', 'Zeit') 

              
'''
ZEIT PROGRAMMENDE
'''
hauptprogramm_monitoring.laufzeit_bestimmen(True)
'''
FINISH
'''
print('FINISH')
