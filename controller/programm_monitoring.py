# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:26:19 2022

@author: Fabian Kayatz
"""

import numpy as np
import datetime

class ProgrammLaufzeit():
    '''Klasse zur Überwachung und Bestimmung der Ausfuehrungszeit eines Programms bzw. Programmteils'''
    
    def __init__(self, bezeichnung, laufzeitstart = np.nan, laufzeit=0):
        self.bezeichnung = bezeichnung
        self.laufzeitstart = laufzeitstart
        self.laufzeit = laufzeit
        
    def startzeit_definieren(self, wert_anzeigen = False):
        self.laufzeitstart = datetime.datetime.now()
        
        if wert_anzeigen == True:
            print(self.bezeichnung, 'Startzeit:', self.laufzeitstart)
    
    def laufzeit_bestimmen(self, wert_anzeigen = False):
        self.laufzeit = datetime.datetime.now() - self.laufzeitstart
        
        if wert_anzeigen == True:
            print(self.bezeichnung, 'Laufzeit:', self.laufzeit)