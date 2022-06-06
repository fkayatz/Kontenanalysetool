# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:26:27 2022

@author: Fabian Kayatz
"""
import datetime

#heutiges Datum bestimmen
def heutiges_datum_bestimmen():
    heutiges_datum=datetime.date.today()
    return(heutiges_datum)

#Bestimmen des letzten Tags im Monat
def letzter_tag_im_monat_bestimmen(date):
    letzter_tag_im_monat=(date + datetime.timedelta(days=31)).replace(day=1)-datetime.timedelta(days=1)
    return(letzter_tag_im_monat)