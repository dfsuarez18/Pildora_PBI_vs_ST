import time
import streamlit as st
import pandas as pd
import numpy as np
from numba import njit
from utils.global_conf import *
from pages.st_top_navbar import *

# Methods with cache data for larger calculations
@st.cache_data(show_spinner='Calculando totales...')
def compute_totals(flights: pd.DataFrame):
    
    return {
        'total_distance': int(flights['distance_km'].sum(axis=0, skipna=True)),
        'total_price': int(flights['totalFare'].sum(axis=0, skipna=True)),
        'total_flights': len(flights)
    }

@st.cache_data(show_spinner='Cargando la tabla de detalles...')
def show_details_table(data: pd.DataFrame, selected_columns: list, format_columns: list):
    st.dataframe(
        data=data[selected_columns].head(500000),
        column_config=format_columns,
        height=None,
        hide_index=True
    )

def container_results(title: str, result: int):
    
    formatted_result = "{:,}".format(result).replace(",", ".")
                                                     
    with st.container(height=130, border=True):
        _, col2, _ = st.columns([1, 6, 1])
        
        with col2:
            st.markdown(
                f'<div style="text-align: center;">'
                f'<p style="font-size:20px; color:{PRIMARY_COLOR}; margin-bottom:0;">'
                f'<strong>{title}</strong></p></div>',
                unsafe_allow_html=True
            )
            
            st.markdown(
                f'<div style="text-align: center;">'
                f'<p style="font-size:32px; color:{PRIMARY_COLOR}; margin-top:0;">'
                f'{formatted_result}</p></div>',
                unsafe_allow_html=True
            )

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

# Get totals
totals = compute_totals(flights[['distance_km', 'totalFare']])
total_distance = totals['total_distance']
total_price = totals['total_price']
total_flights = totals['total_flights']

# Page configuration

_, col1, col2, col3, _ = st.columns([1,2,2,2,1])

with col1:
    container_results("Número total de Vuelos", total_flights)
with col2: 
    container_results("Km totales recorridos", total_distance)
with col3:
    container_results("Precio total billetes", total_price)
        
st.title('Tabla Detalle de Vuelos')
show_details_table(flights, flight_columns, flight_columns_format)