# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 21:05:09 2022

@author: Fabian Kayatz
"""
import plotly.graph_objects as go
import pandas as pd

def create_sankey_plot(df_1,df_2):

    df_fig=pd.concat([df_1,df_2], axis=0)
    label_fig=list(df_1.index)+['Umsatz']+list(df_2.index)
    source_fig= list(range(0,len(df_1),1))+len(df_2)*[len(df_1)]
    target_fig=len(df_1)*[len(df_1)]+list(range(len(df_1)+1,len(df_1)+len(df_2)+1,1))
    value_fig=list(df_fig)
    
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