# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:44:32 2018

Python project
@author: Arnab
Computing ID : as3uj

"""
import csv
import pandas as pd
import numpy as np
import re
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

data = pd.read_csv('D:\Python\Project\CompleteDataset.csv', encoding='utf-8') 
 
#data['Wage(TEUR)'] = data['Wage'].map(lambda x : re.sub('[^0-9]+', '', x)).astype('float64')
#data['Value(MEUR)'] = data['Value'].map(lambda x : re.sub('[^0-9]+', '', x)).astype('float64')

# Function to convert alphanumeric wage and value fields to new numeric fields
  
def str2number(amount):
    if amount[-1] == 'M':
        return float(amount[1:-1])*1000000
    elif amount[-1] == 'K':
        return float(amount[1:-1])*1000
    else:
        return float(amount[1:])
    
# Applying the function to create the numeric value columns for Wage and Value
        
data['ValueNum'] = data['Value'].apply(lambda x: str2number(x))
data['WageNum'] = data['Wage'].apply(lambda x: str2number(x))

data_top1000 = data[:1000] # Getting data rows for top 1000 players

# Grouping the data by Age as index and displaying Value and Wage as per age groups  
age_wagevalue = data_top1000[data_top1000.Age<=38].groupby(['Age']).agg({'WageNum': 'mean', 'ValueNum': 'mean'})      

# Plotting Value over Age with Line and Bar
                                   
data_plot1 = [
    go.Scatter(
        x=age_wagevalue.index, 
        y=age_wagevalue['ValueNum'],
        marker = dict(
          color = 'rgb(0,0,153)'
        ),
                name = "Average Player Value as Line"
            ),
    go.Bar(
        x = age_wagevalue.index,
        y=age_wagevalue['ValueNum'],
        base = 0,
        marker = dict(
          color = 'rgb(51,153,255)'
        ),
                name = "Average Player Value as Bars"
    )
]

layout_plot1 = go.Layout(
    title='Value of players over Age',
    yaxis=dict(title='Average Player Value in Euros(Millions)'),
    xaxis=dict(title='Player Age')
)

fig1 = go.Figure(data=data_plot1, layout=layout_plot1)
    
py.plot(fig1,filename ='Value of players over Age.html')

# Plotting Wage over Age with Line and Bar
                                   
data_plot2 = [
    go.Scatter(
        x=age_wagevalue.index, 
        y=age_wagevalue['WageNum'],
        marker = dict(
          color = 'rgb(0,204,204)'
        ),
                name = "Average Player Wage as Line"
            ),
    go.Bar(
        x = age_wagevalue.index,
        y=age_wagevalue['WageNum'],
        base = 0,
        marker = dict(
          color = 'rgb(0,102,102)'
        ),
                name = "Average Player Wage as Bars"
    )
]

layout_plot2 = go.Layout(
    title='Monthly Wage of players over Age',
    yaxis=dict(title='Average Montly Wage in Euros(Thousands)'),
    xaxis=dict(title='Player Age'),
    )

fig2 = go.Figure(data=data_plot2, layout=layout_plot2)
    
py.plot(fig2,filename ='Monthly Wage of players over Age.html')

# Violin Plot for Value over Age

data_plot3 = []
for i in range(0,len(pd.unique(data_top1000['Age']))):
    trace = {
            "type": 'violin',
            "x": data_top1000['Age'][data_top1000['Age'] == pd.unique(data_top1000['Age'])[i]],
            "y": data_top1000['ValueNum'][data_top1000['Age'] == pd.unique(data_top1000['Age'])[i]],
            "name": pd.unique(data_top1000['Age'])[i],
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
    data_plot3.append(trace)

        
fig3 = {
    "data": data_plot3,
    "layout" : {
        "title": "Distribution of Player Value over Player Age",
        "yaxis": {
            "zeroline": False,
            "title":"Player Value in Euros(Millions)" 
        },
        "xaxis": {
                "title":"Player Age"}
    }
}

py.plot(fig3, filename='Value_Age_Violin.html', validate = False)

# Violin Plot for Wage over Age

data_plot4 = []
for i in range(0,len(pd.unique(data_top1000['Age']))):
    trace = {
            "type": 'violin',
            "x": data_top1000['Age'][data_top1000['Age'] == pd.unique(data_top1000['Age'])[i]],
            "y": data_top1000['WageNum'][data_top1000['Age'] == pd.unique(data_top1000['Age'])[i]],
            "name": pd.unique(data_top1000['Age'])[i],
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
    data_plot4.append(trace)

        
fig4 = {
    "data": data_plot4,
    "layout" : {
        "title": "Distribution of Player Wage over Player Age",
        "yaxis": {
            "zeroline": False,
        "title":"Montly Wage in Euros(Thousands)" 
        },
        "xaxis": {
                "title":"Player Age"
                }
    }
    }


py.plot(fig4, filename='Wage_Age_Violin.html', validate = False)

# Box Plot of Player Value over each position

# Splitting the string value of Preferred Positions into a list of each preffered position for that player
data['Preferred Positions'] = list(map(lambda x: x.split(), data['Preferred Positions']))

# Boolean Function to take a list of positions as input and compare it with a single position and return boolean
def in_preferred_position(list_pos, pos):
    if pos in list_pos:
        return True
    return False

# Applying the above in_preferred_position function to create dataframes for each position 
CAM = data[[in_preferred_position(x, 'CAM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
CAM["PPos"] = "Central Attacking Midfielder"

CB = data[[in_preferred_position(x, 'CB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
CB["PPos"] = "Center Back"

CDM = data[[in_preferred_position(x, 'CDM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
CDM["PPos"] = "Central Defensive Midfielder"

CF = data[[in_preferred_position(x, 'CF') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
CF["PPos"] = "Center Forward"

CM = data[[in_preferred_position(x, 'CM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
CM["PPos"] = "Central Midfielder"

#LAM = data[[in_preferred_position(x, 'LAM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
#LAM["PPos"] = "Left Attacking Midfielder"

LB = data[[in_preferred_position(x, 'LB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
LB["PPos"] = "Left Back"
#LCB = data[[in_preferred_position(x, 'LCB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#LCM = data[[in_preferred_position(x, 'LCM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#LDM = data[[in_preferred_position(x, 'LDM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#LF = data[[in_preferred_position(x, 'LF') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

LM = data[[in_preferred_position(x, 'LM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
LM["PPos"] = "Left Midfielder"
#LS = data[[in_preferred_position(x, 'LS') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

LW = data[[in_preferred_position(x, 'LW') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
LW["PPos"] = "Left Wing"

LWB = data[[in_preferred_position(x, 'LWB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
LWB["PPos"] = "Left Wing Back"

#RAM = data[[in_preferred_position(x, 'RAM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

RB = data[[in_preferred_position(x, 'RB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
RB["PPos"] = "Right Back"
#RCB = data[[in_preferred_position(x, 'RCB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#RCM = data[[in_preferred_position(x, 'RCM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#RDM = data[[in_preferred_position(x, 'RDM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

#RF = data[[in_preferred_position(x, 'RF') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

RM = data[[in_preferred_position(x, 'RM') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
RM["PPos"] = "Right Midfielder"
#RS = data[[in_preferred_position(x, 'RS') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]

RW = data[[in_preferred_position(x, 'RW') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
RW["PPos"] = "Right Wing"

RWB = data[[in_preferred_position(x, 'RWB') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
RWB["PPos"] = "Right Wing Back"

ST = data[[in_preferred_position(x, 'ST') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
ST["PPos"] = "Striker"

GK = data[[in_preferred_position(x, 'GK') for x in data['Preferred Positions']]].sort_values(by="ValueNum",ascending=False)[:200]
GK["PPos"] = "Goal Keeper"
#all_pos = [CAM,CB,CDM,CF,CM,LAM,LB,LCB,LCM,LDM,LF,LM,LS,LW,LWB,RAM,RB,RCB,RCM,RDM,RF,RM,RS,RW,RWB,ST]

#all_pos = [CAM,CB,CDM,CF,CM,LB,LM,LW,LWB,RB,RM,RW,RWB,ST,GK]

#all_pos_vf = pd.concat(all_pos)

#plot_pos = go.Box( y=all_pos_vf[ValueNum], name=col, showlegend=False )

# Creating traces for each position for the box plot

trace1 = go.Box(
    y = LW["ValueNum"],
    name = "Left Wing Forward",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,204,102)'),
    line = dict(
        color = 'rgb(0,204,102)')
)

trace2 = go.Box(
    y = LM["ValueNum"],
    name = "Left Midfielder",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,204,204)'),
    line = dict(
        color = 'rgb(0,204,204)')
)  

trace3 = go.Box(
    y = LWB["ValueNum"],
    name = "Left Wing Back",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,153,153)'),
    line = dict(
        color = 'rgb(0,153,153)')
)

trace4 = go.Box(
    y = LB["ValueNum"],
    name = "Left Back",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,102,102)'),
    line = dict(
        color = 'rgb(0,102,102)')
)      

trace5 = go.Box(
    y = CF["ValueNum"],
    name = "Center Forward",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(102,102,255)'),
    line = dict(
        color = 'rgb(102,102,255)')
)

trace6 = go.Box(
    y = CAM["ValueNum"],
    name = "Central Attacking Midfielder",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(51,51,255)'),
    line = dict(
        color = 'rgb(51,51,255)')
)  

trace7 = go.Box(
    y = CM["ValueNum"],
    name = "Central Midfielder",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,0,204)'),
    line = dict(
        color = 'rgb(0,0,204)')
)

trace8 = go.Box(
    y = CDM["ValueNum"],
    name = "Central Defensive Midfielder",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,0,153)'),
    line = dict(
        color = 'rgb(0,0,153)')
)
    
trace9 = go.Box(
    y = CB["ValueNum"],
    name = "Center Back",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,0,153)'),
    line = dict(
        color = 'rgb(0,0,153)')
)    

trace10 = go.Box(
    y = RW["ValueNum"],
    name = "Right Wing Forward",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,128,255)'),
    line = dict(
        color = 'rgb(0,128,255)')
)  

trace11 = go.Box(
    y = RM["ValueNum"],
    name = "Right Midfielder",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,102,204)'),
    line = dict(
        color = 'rgb(0,102,204)')
)

trace12 = go.Box(
    y = RWB["ValueNum"],
    name = "Right Wing Back",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,76,153)'),
    line = dict(
        color = 'rgb(0,76,153)')
)
    
trace13 = go.Box(
    y = RB["ValueNum"],
    name = "Right Back",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,51,102)'),
    line = dict(
        color = 'rgb(0,51,102)')
)      

trace14 = go.Box(
    y = ST["ValueNum"],
    name = "Striker",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(0,102,53)'),
    line = dict(
        color = 'rgb(0,102,53)')
)
    
trace15 = go.Box(
    y = GK["ValueNum"],
    name = "Goal Keeper",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(102,0,102)'),
    line = dict(
        color = 'rgb(102,0,102)')
)    
data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15]

layout = go.Layout(
    title = "Player Value at Different Positions"
)

fig = go.Figure(data=data,layout=layout)
py.plot(fig, filename = "Value over Position.html")

