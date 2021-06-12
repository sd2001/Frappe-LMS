import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


def member_bar_plot(names, spend):
    data = [go.Bar(x = names,y = spend, textposition='auto', marker_color='lightsalmon', text=spend)]
    
    
    fig1 = go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text="Bar Chart: Net Expenditure of Members")))
    fig1.update_layout(font_family="Arial",
                       title_font_color="RebeccaPurple",
                       title_font_family="Courier New, monospace",
                       title={
						'y':0.9,
						'x':0.5,
						'xanchor': 'center',
						'yanchor': 'top'})
    fig1.update_xaxes(title_text='Name of Members')
    fig1.update_yaxes(title_text='Net Spend')
    
    return fig1

def member_pie_plot(names, spend):
    data = [go.Pie(labels = names,values = spend, textinfo='label+percent', hole=.4)]
    
    
    fig2 = go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text="Pie Chart: Net Expenditure of Members")))
    fig2.update_layout(font_family="Arial",
                       title_font_color="RebeccaPurple",
                       title_font_family="Courier New, monospace",
                       title={
						'y':0.9,
						'x':0.5,
						'xanchor': 'center',
						'yanchor': 'top'})
    fig2.update_xaxes(title_text='Name of Members')
    fig2.update_yaxes(title_text='Net Spend')
    
    return fig2
 