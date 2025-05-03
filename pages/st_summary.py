import streamlit as st
import pandas as pd
from utils.global_conf import *
from utils.graph_functions import *
from pages.st_top_navbar import *

# -----------------------------Data configuration----------------------------------

flights_columns_to_select = [
    'flight_id',
    'airlineCode',
    'model',
    'departure_date',
    'departureAirportCode',
    'totalFare',
    'distance_km'
]

airports_columns_to_select = [
    'code',
    'name',
    'city',
    'state',
    'latitude',
    'longitude'
]

flights = pd.DataFrame(st.session_state[FLIGHTS], columns=flights_columns_to_select)
airports = pd.DataFrame(st.session_state[AIRPORTS], columns=airports_columns_to_select)

# Change Type of columns
flights[['totalFare', 'distance_km']] = (
    flights[['totalFare', 'distance_km']]
    .replace(',', '.', regex=True)
    .apply(pd.to_numeric)
)

flights[['departure_date']] = flights[['departure_date']].apply(pd.to_datetime)

# Map airlines names
dictionary_airlines = dict(pd.DataFrame(st.session_state[AIRLINES], columns=['airlineCode', 'airlineName']).values)
flights['airlineName'] = flights['airlineCode'].map(dictionary_airlines)

# Dataframes with the number of flights per airline / model
airline_counts = flights['airlineName'].value_counts().reset_index()
airline_counts.columns = ['airlineName', 'numFlights']
airline_counts.sort_values('numFlights', ascending=False)
airline_counts = airline_counts[['numFlights', 'airlineName']]

model_counts = flights['model'].value_counts().reset_index()
model_counts.columns = ['model', 'numFlights']
model_counts.sort_values('numFlights', ascending=False)
model_counts = model_counts[['numFlights', 'model']]

# Dataframes with the top 10 airlines / models by distance
top_airlines_by_distance = (
    flights.groupby('airlineName')['distance_km']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    .rename(columns={'distance_km': 'totalDistance'})
)

top_models_by_distance = (
    flights.groupby('model')['distance_km']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    .rename(columns={'distance_km': 'totalDistance'})
)

# Dataframe with the Price evolution
price_evolution = (
    flights.groupby('departure_date')['totalFare']
    .mean()
    .reset_index()
    .rename(columns={'totalFare': 'avg_price'})
)
price_evolution = price_evolution[['departure_date', 'avg_price']]
price_evolution.sort_values('departure_date', ascending=True)
avg_price = float(price_evolution['avg_price'].mean())

# Dataframe with the location information

flights_locations = flights[['departureAirportCode']]
flights_locations.columns = ['code']
flights_locations = flights_locations['code'].value_counts().reset_index()

dictionary_states = dict(pd.DataFrame(st.session_state[CITIES], columns=['state_code', 'state_name']).values)
airports['state_name'] = airports['state'].map(dictionary_states)
flights_locations= pd.merge(flights_locations, airports, on='code', how='left', validate='many_to_many')

# -----------------------------Page Configuration----------------------------------

col1, col2 = st.columns(2)

with col1:
    
    model_selected = RADIO_AIRLINE_MODEL_KEY in st.session_state and st.session_state[RADIO_AIRLINE_MODEL_KEY] == RADIO_AIRLINE_MODEL_OPTIONS[1]
    
    # Graph with the number of flights by airline/model
    if model_selected:
        st.plotly_chart(horizontal_bars_graph(
            'Número de vuelos por aerolínea',
            'Número de Vuelos',
            'Aerolínea',
            airline_counts
        ))
    else:
        st.plotly_chart(horizontal_bars_graph(
            'Número de vuelos por modelo de avión',
            'Número de Vuelos',
            'Modelo',
            model_counts
        ))
        
    # Radio button to select show info of airlines or models
    st.session_state[RADIO_AIRLINE_MODEL_KEY] = st.radio(
        label='Visualization Mode', 
        options=RADIO_AIRLINE_MODEL_OPTIONS, 
        horizontal=True, 
        label_visibility='hidden')
    
    # Graph with the top airlines/models by Km
    if model_selected:
        st.plotly_chart(pie_chart(
            'Top 10 aerolineas por km recorridos',
            'Airline Name',
            'Sum of Km',
            top_airlines_by_distance
        ))
    else:
        st.plotly_chart(pie_chart(
            'Top 10 modelos de avión por km recorridos',
            'Modelo',
            'Sum of Km',
            top_models_by_distance
        ))

with col2:
    st.plotly_chart(buble_chart_map(
        'Número de salidas por ciudad',
        'state_name',
        'name',
        'count',
        'latitude',
        'longitude',
        flights_locations
    ))
    
    st.plotly_chart(line_graph_with_avg(
        'Evolución temporal del precio medio de un billete', 'Fecha', 'Precio total', 'Precio Medio', price_evolution, avg_price
    ))
