# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 21:05:09 2022

@author: Fabian Kayatz
"""
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
    
def saeulendiagramm_erstellen(df, titel, ylabel):
    
    #Prüfen ob Index ein Zeitformat ist und dann ins gewünschte Format ändern
    if type(df.index) == pd.DatetimeIndex:
        labels = df.index.strftime(date_format='%m/%y').tolist()
    else:
        labels = df.index
        
    list_messreihen=df.columns.tolist()
    #Graphparameter
    saeulenbreite=0.8/len(list_messreihen)
    x = list(np.arange(len(labels)))  # the label locations
    
    #Definition des Diagramms
    fig, ax=plt.subplots()
    fig.tight_layout()
    
    #Einfügen des Messreihen
    for messreihe in list_messreihen:
        pos_messreihe=list_messreihen.index(messreihe)
        pos_x=np.array(x)-saeulenbreite*((len(list_messreihen)-1)/2-pos_messreihe)
        ax.bar(pos_x,df[str(messreihe)], saeulenbreite, label=str(messreihe))
        
    #Formatierung des Graphen
    ax.set_ylabel(ylabel)
    ax.set_title(titel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.tick_params(axis='x',labelrotation=90)
    ax.legend()
    ax.grid(True, linestyle='--')
    
    #Darstellung des Graphs
    plt.show()
    
    return()

'''
fig1 = px.bar(df_auswertung_pro_monat, 
              x=df_auswertung_pro_monat.index,
              y=['Einnahmen', 'Ausgaben'],
              title='Einnahmen & Ausgaben',
              #xaxis_title="X Axis Title",
              #yaxis_title="Wert in €",
              #labels={y:'Wert in €'},
              #color='Einnahmen'
              )    
fig1.show(renderer='svg') # =browser oder svg (Anzeige in Spyder)
'''

def liniendiagramm_erstellen(df_x, df_y, titel, ylabel, xlabel):
    
    #Prüfen ob Index ein Zeitformat ist und dann ins gewünschte Format ändern
    if type(df_x) == pd.DatetimeIndex:
        labels = df_x.strftime(date_format='%m/%y').tolist()
    else:
        labels = df_x   
        
    #Definition des Diagramms
    fig, ax = plt.subplots()

    #Einfügen der Messreihen
    ax.plot(labels,df_y, linewidth=2.0)

    #Formatierung des Graphen
    ax.set_ylabel(ylabel)
    ax.set_title(titel)
    ax.tick_params(axis='x',labelrotation=90)
    ax.legend(df_y.columns)
    ax.grid(True, linestyle='--')
    
    #Darstellung des Graphs
    plt.show()
    
    return()
    

def create_sankey_plot(df_1,df_2):

    label_fig=list(df_1.index)+['Umsatz']+list(df_2.index)
    source_fig= list(range(0,len(df_1),1))+len(df_2)*[len(df_1)]
    target_fig=len(df_1)*[len(df_1)]+list(range(len(df_1)+1,len(df_1)+len(df_2)+1,1))
    value_fig=list(pd.concat([df_1,df_2], axis=0))
    
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = label_fig,
      color = "black"
    ),
    link = dict(
      source = source_fig, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = target_fig,
      value = value_fig
      ))])
    
    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    fig.show(renderer='browser')
    
    return()

def saeulen_linien_diagramm_erstellen(x,df_saeulen, df_linien, df_linien_stabw, titel, ylabel):
    
    #Prüfen ob Index ein Zeitformat ist und dann ins gewünschte Format ändern
    if type(x) == pd.DatetimeIndex:
        labels = x.strftime(date_format='%m/%y').tolist()
    else:
        labels = x   
    
    #Definition des Diagramms
    fig, ax=plt.subplots()
    fig.tight_layout()
    
    #Einfügen das Säulendiagramm
    ax.bar(labels,df_saeulen,0.8)
    
    #Einfügen des Liniendiagramm
    ax.plot(labels,df_linien, linewidth=2.0)
    
    #Einfügen der Standardabweichung und Ausfüllen
    y1=df_linien-df_linien_stabw
    y2=df_linien+df_linien_stabw
    
    ax.fill_between(labels, y1, y2, alpha=.5, linewidth=0)
    
    #Formatierung des Graphen
    ax.set_ylabel(ylabel)
    ax.set_title(titel)
    ax.tick_params(axis='x',labelrotation=90)
    #ax.legend(df_y.columns)
    ax.grid(True, linestyle='--')
    
    #Darstellung des Graphs
    plt.show()
    
    return()

# Liniendiagramm mit Füllbereich
def liniendiagramm_mit_fuellbereich_erstellen(df_x, df_y, df_yfill, titel, ylabel, xlabel):
    
    #Prüfen ob Index ein Zeitformat ist und dann ins gewünschte Format ändern
    if type(df_x) == pd.DatetimeIndex:
        labels = df_x.strftime(date_format='%m/%y').tolist()
    else:
        labels = df_x   
        
    #Definition des Diagramms
    fig, ax = plt.subplots()

    #Einfügen der Messreihen
    ax.plot(labels,df_y, linewidth=2.0)
    
    #Einfügen der Füllbereiche
    for i in range(0,len(df_yfill.columns),1):

        if i == 0:
            ax.fill_between(labels, 0, df_yfill.iloc[:,i], alpha=.5, linewidth=0)
        else:
            ax.fill_between(labels, df_yfill.iloc[:,i-1], df_yfill.iloc[:,i], alpha=.5, linewidth=0)
        i=i+1
        
    #Formatierung des Graphen
    ax.set_ylabel(ylabel)
    ax.set_title(titel)
    ax.tick_params(axis='x',labelrotation=90)
    ax.legend(list(df_y.columns) + list(df_yfill.columns))
    ax.grid(True, linestyle='--')
    
    #Darstellung des Graphs
    plt.show()
    
    return()

# run if the file is directly executed
if __name__ == "__main__":
    print(__name__)