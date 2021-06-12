import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

def book_pie_plot(names, issues):
    data = [go.Pie(labels = names,values = issues, textinfo='label+percent', hole=.4)]
    
    
    fig1 = go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text="Pie Chart: Most Issued Books")))
    fig1.update_layout(width=600, height=600,
                       font_family="Arial",
                       title_font_color="RebeccaPurple",
                       title_font_family="Courier New, monospace",title={
						'y':0.9,
						'x':0.5,
						'xanchor': 'center',
						'yanchor': 'top'})
    fig1.update_xaxes(title_text='Name of Books')
    fig1.update_yaxes(title_text='Net Issues')
    
    return fig1

def book_line_plot(names, issues):
    data = [go.Scatter(x = names, y = issues, mode='lines+markers', line_color='rgb(0,100,80)')]
    fig2 = go.Figure(data=data, layout=go.Layout(title=go.layout.Title(text="Line Chart: Most Issued Books")))
    fig2.update_layout(width=600, height=600,
                       font_family="Arial",
                       title_font_color="RebeccaPurple",
                       title_font_family="Courier New, monospace",
                       title={
						'y':0.9,
						'x':0.5,
						'xanchor': 'center',
						'yanchor': 'top'})
    fig2.update_xaxes(title_text='Name of Books', title_font = {"size": 20})
    fig2.update_yaxes(title_text='Net Issues', title_font = {"size": 20})
    
    return fig2
    
 
 