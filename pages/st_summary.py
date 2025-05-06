import streamlit as st
import pandas as pd
from utils.global_conf import *
from utils.graph_functions import *
from utils.filter_functions import *
from pages.st_top_navbar import *
from streamlit_folium import folium_static

# -----------------------------Data configuration----------------------------------

# Show and apply selected filters
show_logo()
show_filters()
flights = apply_filters()

airports_columns_to_select = [
    'code',
    'name',
    'city',
    'state',
    'latitude',
    'longitude'
]

airports = pd.DataFrame(st.session_state[AIRPORTS], columns=airports_columns_to_select)

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
flights_locations = pd.merge(flights_locations, airports, on='code', how='left', validate='many_to_many')
flights_locations = flights_locations.dropna(axis=0)

# -----------------------------Page Configuration----------------------------------

col1, col2 = st.columns(2)

with col1:
    
    # Radio button to select show info of airlines or models
    st.session_state[RADIO_AIRLINE_MODEL_KEY] = st.radio(
        label='Visualization Mode', 
        options=RADIO_AIRLINE_MODEL_OPTIONS, 
        horizontal=True, 
        label_visibility='collapsed')
    
    # Graph with the number of flights by airline/model
    if RADIO_AIRLINE_MODEL_KEY not in st.session_state or st.session_state[RADIO_AIRLINE_MODEL_KEY] == RADIO_AIRLINE_MODEL_OPTIONS[0]:
        st.plotly_chart(horizontal_bars_graph(
            'Número de vuelos por aerolínea',
            'Número de Vuelos',
            'Aerolínea',
            airline_counts,
            PRIMARY_COLOR
        ))
    else:
        st.plotly_chart(horizontal_bars_graph(
            'Número de vuelos por modelo de avión',
            'Número de Vuelos',
            'Modelo',
            model_counts,
            PRIMARY_COLOR
        ))
    
    # Graph with the top airlines/models by Km
    if RADIO_AIRLINE_MODEL_KEY not in st.session_state or st.session_state[RADIO_AIRLINE_MODEL_KEY] == RADIO_AIRLINE_MODEL_OPTIONS[0]:
        st.plotly_chart(pie_chart(
            'Top 10 aerolineas por km recorridos',
            'Airline Name',
            'Sum of Km',
            top_airlines_by_distance,
            GRAPH_COLOR_LIST
        ))
    else:
        st.plotly_chart(pie_chart(
            'Top 10 modelos de avión por km recorridos',
            'Modelo',
            'Sum of Km',
            top_models_by_distance,
            GRAPH_COLOR_LIST
        ))

with col2:
    
    # Bubble Map of Departures by City
    st.write("")
    st.markdown("**Mapa de salidas por aeropuerto**")
    
    popup_info = {'Aeropuerto': 'name', 'Ciudad': 'city', 'Estado': 'state_name', 'Num. salidas': 'count'}
    folium_static(
        bubble_chart_map(
        popup_info,
        'count',
        'latitude',
        'longitude',
        flights_locations,
        PRIMARY_COLOR
    ), height=425)
    
    st.plotly_chart(line_graph_with_avg(
        'Evolución temporal del precio medio de un billete', 'Fecha', 'Precio total', 'Precio Medio', 
        price_evolution, avg_price, PRIMARY_COLOR, SECONDARY_COLOR
    ))
