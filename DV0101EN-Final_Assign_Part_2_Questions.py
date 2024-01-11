#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the layout of the app
year_list = [i for i in range(1980, 2024, 1)]

options='dropdown_options' 
app.layout = html.Div([
    # Title
    html.H1(
        'Automobile Sales Statistics Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 24
        }
    ),
    # Dropdown for selecting report type
    dcc.Dropdown(id='dropdown-statistics',
                dropdown_options = [
                                   {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                                   {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                                   ]
               placeholder='Select a report type',
               value='Select Statistics',
               style={'width': '80%', 'padding': '3px', 'font size': '20px', 'text-align-last':'center'}
    ),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        html.Div(dcc.Dropdown(
                    id='select-year',
                    options=[{'label': i, 'value': i} for i in year_list],
                    value='Select-year'
                )),
    ),
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),])
    ])


# Callback to enable or disable the year dropdown based on the selected report type
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to plot the output graphs for the respective report types
@app.callback(

    Output(component_id='output-container', component_property='children'),

    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value') ])

def update_output_container(selected_statistics, input_year):
    # Initialize an empty list to store the generated graphs
    graphs = []

    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over the Recession Period (year-wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales Fluctuation Over Recession Period (Year Wise)"
            )
        )
        

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a bar chart
        avg_sales_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales_by_type,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type"
            )
        )
        

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Expenditure Share by Vehicle Type During Recessions"
            )
        )
        

        # Plot 4: Develop a bar chart for the effect of the unemployment rate on vehicle type and sales
        Y_chart4 = dcc.Graph(
            figure=px.bar(
                recession_data,
                x='Unemployment_Rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )
    return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
            ]    

    # Yearly Statistic Report Plots
    elif input_year and selected_statistics == 'Yearly Statistics report':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using a line chart for the whole period
        yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales for the Whole Period'
            )
        )
        

        # Plot 2: Total Monthly Automobile sales using a line chart
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )
        

        # Plot 3: Bar chart for the average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )
        

        # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
        exp_by_vehicle = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.pie(
                exp_by_vehicle,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure by Vehicle Type in the year {}'.format(input_year)
            )
        )
    

    return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
            ]

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
