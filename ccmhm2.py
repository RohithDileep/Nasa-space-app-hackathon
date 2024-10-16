import pandas as pd
import matplotlib.pyplot as plt
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Function to get input from user
def get_input_data():
    # Asking for user input for the dataset or use CSV
    choice = input("Do you want to enter data manually (Y/N) or use a CSV file (type 'csv')? ")
    
    if choice.lower() == 'y':
        # Input Climate Data
        regions = []
        years = []
        avg_temps = []
        rainfalls = []
        drought_days = []
        
        maternal_mortalities = []
        birth_complications = []

        n = int(input("Enter the number of regions: "))

        for i in range(n):
            region = input(f"Enter Region {i+1} name: ")
            year = int(input(f"Enter Year for {region}: "))
            avg_temp = float(input(f"Enter Average Temperature for {region}: "))
            rainfall = float(input(f"Enter Rainfall (in mm) for {region}: "))
            drought = int(input(f"Enter Number of Drought Days for {region}: "))

            maternal_mortality = int(input(f"Enter Maternal Mortality Rate for {region}: "))
            birth_complication = float(input(f"Enter Birth Complications (%) for {region}: "))
            
            regions.append(region)
            years.append(year)
            avg_temps.append(avg_temp)
            rainfalls.append(rainfall)
            drought_days.append(drought)

            maternal_mortalities.append(maternal_mortality)
            birth_complications.append(birth_complication)
        
        # Create DataFrame
        climate_data = pd.DataFrame({
            'Region': regions,
            'Year': years,
            'Avg_Temperature': avg_temps,
            'Rainfall': rainfalls,
            'Drought_Days': drought_days
        })
        
        maternal_health_data = pd.DataFrame({
            'Region': regions,
            'Year': years,
            'Maternal_Mortality_Rate': maternal_mortalities,
            'Birth_Complications': birth_complications
        })
        
    elif choice.lower() == 'csv':
        # Input via CSV files
        climate_csv = input("Enter the path of the climate data CSV file: ")
        maternal_csv = input("Enter the path of the maternal health data CSV file: ")
        
        climate_data = pd.read_csv(climate_csv)
        maternal_health_data = pd.read_csv(maternal_csv)
    
    else:
        print("Invalid input! Exiting...")
        exit()
    
    return climate_data, maternal_health_data


# Main function to prepare data and visualization
def prepare_data():
    # Get input data
    climate_df, maternal_df = get_input_data()
    
    # Merge the two dataframes
    merged_df = pd.merge(climate_df, maternal_df, on=['Region', 'Year'])
    
    return merged_df


# Plot Correlation between temperature and maternal mortality
def plot_correlation(df):
    plt.scatter(df['Avg_Temperature'], df['Maternal_Mortality_Rate'])
    plt.xlabel('Average Temperature (°C)')
    plt.ylabel('Maternal Mortality Rate (per 100,000)')
    plt.title('Temperature vs Maternal Mortality')
    plt.show()


# Dash Web Application
def run_dashboard(merged_df):
    app = dash.Dash(_name_, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    app.layout = dbc.Container([
        html.H1('Climate Change & Maternal Health Monitoring'),

        # Dropdown to select Region
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in merged_df['Region'].unique()],
            value=merged_df['Region'].unique()[0]
        ),

        # Graph placeholder
        dcc.Graph(id='maternal-health-graph')
    ])

    # Update Graph based on selected region
    @app.callback(
        Output('maternal-health-graph', 'figure'),
        [Input('region-dropdown', 'value')]
    )
    def update_graph(selected_region):
        filtered_df = merged_df[merged_df['Region'] == selected_region]

        fig = {
            'data': [
                {'x': filtered_df['Year'], 'y': filtered_df['Avg_Temperature'], 'type': 'line', 'name': 'Temperature'},
                {'x': filtered_df['Year'], 'y': filtered_df['Maternal_Mortality_Rate'], 'type': 'line', 'name': 'Mortality Rate'}
            ],
            'layout': {
                'title': f'Climate and Maternal Health in {selected_region}',
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Value'}
            }
        }
        return fig

    app.run_server(debug=True)


# Main workflow
if _name_ == '_main_':
    # Prepare the data
    merged_df = prepare_data()
    
    # Show correlation plot
    plot_correlation(merged_df)
    
    # Run the dashboard
    run_dashboard(merged_df)
