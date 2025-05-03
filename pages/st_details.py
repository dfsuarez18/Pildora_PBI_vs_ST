import streamlit as st
import pandas as pd
from utils.global_conf import *
from pages.st_top_navbar import *

# Data configuration

flight_columns = [
    'flight_id', 
    'airlineCode', 
    'airlineName',
    'departureAirportCode',
    'departureAirportName',
    'arrivalAirportCode',
    'arrivalAirportName', 
    'model',
    'departureDateTime', 
    'arrivalDateTime', 
    'isNonStop', 
    'isBasicEconomy', 
    'isRefundable', 
    'baseFare', 
    'totalFare', 
    'tax_percent', 
    'cabinCode', 
    'durationInSeconds', 
    'distance_km', 
    'elapsedDays'
]

flight_columns_format = {
    'flight_id': 'Id Vuelo', 
    'airlineCode': 'Cod. Aerolínea', 
    'airlineName': 'Nombre Aerolínea',
    'departureAirportCode': 'Cod. Aeropuerto Salida',
    'departureAirportName': 'Nombre Aeropuerto Salida',
    'arrivalAirportCode': 'Cod. Aeropuerto LLegada',
    'arrivalAirportName': 'Nombre Aeropuerto LLegada', 
    'model': 'Modelo de Avión',
    'departureDateTime': 'Fecha Salida', 
    'arrivalDateTime': 'Fecha LLegada', 
    'isNonStop': 'Sin paradas', 
    'isBasicEconomy': 'Low Cost', 
    'isRefundable': 'Con reembolso', 
    'baseFare': 'Precio Base ($)', 
    'totalFare': 'Precio Total ($)', 
    'tax_percent': '% Impuestos', 
    'cabinCode': 'Tipo Asiento', 
    'durationInSeconds': 'Duración (h)', 
    'distance_km': 'Distancia (Km)', 
    'elapsedDays': 'Dias Transcurridos'
}

flight_columns_numeric = [
    'baseFare',
    'totalFare',
    'tax_percent',
    'durationInSeconds',
    'distance_km', 
    'elapsedDays'
]

flights = pd.DataFrame(st.session_state[FLIGHTS])
flight_columns_exclude = list(flights.columns)

# Change Type of numeric columns
flights[flight_columns_numeric] = (
    flights[flight_columns_numeric]
    .replace(',', '.', regex=True)
    .apply(pd.to_numeric)
)

# Map airlines names
dictionary_airlines = dict(pd.DataFrame(st.session_state[AIRLINES], columns=['airlineCode', 'airlineName']).values)
flights['airlineName'] = flights['airlineCode'].map(dictionary_airlines)

# Map Airport names
dictionary_airports = dict(pd.DataFrame(st.session_state[AIRPORTS], columns=['code', 'name']).values)
flights['departureAirportName'] = flights['departureAirportCode'].map(dictionary_airports)
flights['arrivalAirportName'] = flights['arrivalAirportCode'].map(dictionary_airports)

# Map boolean values
dictionary_boolean = {'N': 'No', 'Y': 'Si'}
flights['isNonStop'] = flights['isNonStop'].map(dictionary_boolean)
flights['isBasicEconomy'] = flights['isBasicEconomy'].map(dictionary_boolean)
flights['isRefundable'] = flights['isRefundable'].map(dictionary_boolean)

# Map duration
flights['durationInSeconds'] = flights['durationInSeconds'].apply(lambda x: x/60/60)

# Map dates and times
flights['departureDateTime'] = pd.to_datetime(flights['departure_date'] + ' ' + flights['departure_time'])
flights['arrivalDateTime'] = pd.to_datetime(flights['arrival_date'] + ' ' + flights['arrival_time'])

flights.info()

# Get totals
total_distance = flights['distance_km'].sum(skipna=True)
total_price = flights['totalFare'].sum(skipna=True)
total_flights = len(flights)

# Page configuration

col1, col2, col3 = st.columns(3)

# TODO: Find a better way to show the distance and price
with col1:
    with st.container(height=150, border=True):
        st.text('Número total de Vuelos')
        st.code(total_flights, wrap_lines=True)

with col2: 
    with st.container(height=150, border=True):
        st.text('Km totales recorridos')
        st.code(total_distance, wrap_lines=True)

with col3: 
    with st.container(height=150, border=True):
        st.text('$ recaudados en vuelos')
        st.code(total_price, wrap_lines=True)
        

st.title('Tabla Detalle de Vuelos')
st.dataframe(
    data=flights[flight_columns].head(50000),
    column_config=flight_columns_format,
    height=None,
    hide_index=True
)