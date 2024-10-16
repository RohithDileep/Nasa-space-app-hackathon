import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Function to create a new CSV file
def create_csv_file(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Temperature', 'Precipitation'])
        writer.writerow(['2022-01-01', 20, 10])
        writer.writerow(['2022-01-02', 22, 12])
        writer.writerow(['2022-01-03', 25, 15])
        writer.writerow(['2022-01-04', 28, 18])
        writer.writerow(['2022-01-05', 30, 20])

# Function to create a new CSV file for gender data
def create_gender_csv_file(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Education Level', 'Employment Rate'])
        writer.writerow(['2022-01-01', 80, 70])
        writer.writerow(['2022-01-02', 82, 72])
        writer.writerow(['2022-01-03', 85, 75])
        writer.writerow(['2022-01-04', 88, 78])
        writer.writerow(['2022-01-05', 90, 80])

# Function to load CSV data
def load_csv_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row)
    return data

# Function to analyze climate data
def analyze_climate_data(data):
    temperatures = [float(row[1]) for row in data]
    precipitations = [float(row[2]) for row in data]
    average_temperature = sum(temperatures) / len(temperatures)
    average_precipitation = sum(precipitations) / len(precipitations)
    print(f"Average temperature: {average_temperature:.2f}°C")
    print(f"Average precipitation: {average_precipitation:.2f} mm")

# Function to analyze gender data
def analyze_gender_data(data):
    education_levels = [float(row[1]) for row in data]
    employment_rates = [float(row[2]) for row in data]
    average_education_level = sum(education_levels) / len(education_levels)
    average_employment_rate = sum(employment_rates) / len(employment_rates)
    print(f"Average education level: {average_education_level:.2f}")
    print(f"Average employment rate: {average_employment_rate:.2f}%")

# Function to visualize data
def visualize_data(data):
    temperatures = [float(row[1]) for row in data]
    precipitations = [float(row[2]) for row in data]
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(temperatures, label='Temperature')
    plt.plot(precipitations, label='Precipitation')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Climate Data')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(temperatures, bins=5, alpha=0.5, label='Temperature')
    plt.hist(precipitations, bins=5, alpha=0.5, label='Precipitation')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Climate Data Distribution')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Function to visualize gender data
def visualize_gender_data(data):
    education_levels = [float(row[1]) for row in data]
    employment_rates = [float(row[2]) for row in data]
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(education_levels, label='Education Level')
    plt.plot(employment_rates, label='Employment Rate')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Gender Data')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(education_levels, bins=5, alpha=0.5, label='Education Level')
    plt.hist(employment_rates, bins=5, alpha=0.5, label='Employment Rate')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Gender Data Distribution')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function
def main():
    print("Climate Resilience and Gender Equality Dashboard")
    print("-----------------------------------------------")
    while True:
        print("1. Create climate data CSV file")
        print("2. Create gender data CSV file")
        print("3. Load and analyze climate data")
        print("4. Load and analyze gender data")
        print("5. Visualize climate data")
        print("6. Visualize gender data")
        print("7. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_csv_file('climate_data.csv')
            print("Climate data CSV file created successfully!")
        elif choice == "2":
            create_gender_csv_file('gender_data.csv')
            print("Gender data CSV file created successfully!")
        elif choice == "3":
            data = load_csv_data('climate_data.csv')
            analyze_climate_data(data)
        elif choice == "4":
            data = load_csv_data('gender_data.csv')
            analyze_gender_data(data)
        elif choice == "5":
            data = load_csv_data('climate_data.csv')
            visualize_data(data)
        elif choice == "6":
            data = load_csv_data('gender_data.csv')
            visualize_gender_data(data)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()

# DASH APP SECTION
app = dash.Dash(_name_)

app.layout = html.Div([
    html.H1('Climate Resilience and Gender Equality Dashboard'),
    dcc.Dropdown(
        id='climate-dropdown',
        options=[
            {'label': 'Temperature', 'value': 'Temperature'},
            {'label': 'Precipitation', 'value': 'Precipitation'}
        ],
        value='Temperature'
    ),
    dcc.Graph(id='climate-graph'),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Education Level', 'value': 'Education Level'},
            {'label': 'Employment Rate', 'value': 'Employment Rate'}
        ],
        value='Education Level'
    ),
    dcc.Graph(id='gender-graph')
])

@app.callback(
    Output('climate-graph', 'figure'),
    [Input('climate-dropdown', 'value')]
)
def update_climate_graph(selected_value):
    data = load_csv_data('climate_data.csv')
    df = {
        "Date": [row[0] for row in data],
        selected_value: [float(row[1 if selected_value == 'Temperature' else 2]) for row in data]
    }
    fig = px.line(df, x='Date', y=selected_value)
    fig.update_layout(title='Climate Trend', xaxis_title='Date', yaxis_title=selected_value)
    return fig

@app.callback(
    Output('gender-graph', 'figure'),
    [Input('gender-dropdown', 'value')]
)
def update_gender_graph(selected_value):
    data = load_csv_data('gender_data.csv')
    df = {
        "Date": [row[0] for row in data],
        selected_value: [float(row[1 if selected_value == 'Education Level' else 2]) for row in data]
    }
    fig = px.bar(df, x='Date', y=selected_value)
    fig.update_layout(title='Population Trend', xaxis_title='Date', yaxis_title=selected_value)
    return fig

if _name_ == "_main_":
    app.run_server(debug=True)
