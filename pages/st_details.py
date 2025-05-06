import streamlit as st
import pandas as pd
from utils.global_conf import *
from utils.filter_functions import *
from pages.st_top_navbar import *

# -----------------------------Functions----------------------------------

def compute_totals(flights: pd.DataFrame):
    
    return {
        'total_distance': int(flights['distance_km'].sum(axis=0, skipna=True)),
        'total_price': int(flights['totalFare'].sum(axis=0, skipna=True)),
        'total_flights': len(flights)
    }

def show_details_table(data: pd.DataFrame, selected_columns: list, format_columns: dict[str, str]):
    st.dataframe(
        data=data[selected_columns].head(500000),
        column_config=format_columns,
        height=None,
        hide_index=True,
        selection_mode='multi-row'
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

# -----------------------------Data Configuration----------------------------------

# Show and apply selected filters
show_logo()
show_filters()
flights = apply_filters()

flight_columns = [
    'flight_id', 
    'airlineCode', 
    'airlineName',
    'departureAirportCode',
    'departureAirportName',
    'arrivalAirportCode',
    'arrivalAirportName', 
    'model',
    'departure_date', 
    'arrival_date',
    'departure_time', 
    'arrival_time', 
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
    'departure_date': 'Fecha de Salida', 
    'arrival_date': 'Fecha de LLegada',
    'departure_time': 'Hora de Salida', 
    'arrival_time': 'Hora de LLegada',
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

# Map boolean values
dictionary_boolean = {'N': 'No', 'Y': 'Si'}
flights['isNonStop'] = flights['isNonStop'].map(dictionary_boolean)
flights['isBasicEconomy'] = flights['isBasicEconomy'].map(dictionary_boolean)
flights['isRefundable'] = flights['isRefundable'].map(dictionary_boolean)

# Map duration
flights['durationInSeconds'] = flights['durationInSeconds'].apply(lambda x: x/60/60)

# Map departure_date
flights['departure_date'] = flights['departure_date'].dt.strftime('%Y-%m-%d')

# Get totals
totals = compute_totals(flights[['distance_km', 'totalFare']])
total_distance = totals['total_distance']
total_price = totals['total_price']
total_flights = totals['total_flights']

# -----------------------------Page Configuration----------------------------------

_, col1, col2, col3, _ = st.columns([1,2,2,2,1])

with col1:
    container_results("Número total de Vuelos", total_flights)
with col2: 
    container_results("Km totales recorridos", total_distance)
with col3:
    container_results("Precio total billetes", total_price)
        
st.title('Tabla Detalle de Vuelos')
show_details_table(flights, flight_columns, flight_columns_format)