# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500',
                                            10000: '10000'},
                                    value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # Get data for selected launch site
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site] 

    if entered_site == 'ALL':
        # piechart for all sites
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df,  
        names='class', 
        title='Total Success Launches for site {}'.format(entered_site),
        color='class',               # MUST be explicitly set to use color_discrete_map
        color_discrete_map={
            0: 'red',            # Maps the value 0 (failure) to light red
            1: 'green'             # Maps the value 1 (success) to light green
        })
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, selected_payload_range):
    # Get payload range from slider
    min_payload, max_payload = selected_payload_range

    # Get data for all launch sites and payload range from slider
    filtered_df_site_all = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) &
                            (spacex_df['Payload Mass (kg)'] <= max_payload)] 

    # Get data for selected launch site and payload range from slider
    filtered_df_site_selected = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                            (spacex_df['Payload Mass (kg)'] >= min_payload) &
                            (spacex_df['Payload Mass (kg)'] <= max_payload)] 

    if entered_site == 'ALL':
        # scatter plot for all sites
        fig = px.scatter(filtered_df_site_all, 
        x='Payload Mass (kg)', 
        y='class', 
        title='Correlation between Payload and Success for all Sites',
        color="Booster Version Category")
        return fig
    else:
        # scatter plot for selected site and payload range
        fig = px.scatter(filtered_df_site_selected, 
        x='Payload Mass (kg)', 
        y='class', 
        title='Correlation between Payload and Success for Site: {}'.format(entered_site),
        color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
