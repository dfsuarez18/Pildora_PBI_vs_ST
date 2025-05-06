import pandas as pd
import streamlit as st

from utils.global_conf import *

flight_columns_numeric = [
    'baseFare',
    'totalFare',
    'tax_percent',
    'durationInSeconds',
    'distance_km', 
    'elapsedDays'
]

@st.cache_data(show_spinner='Transformando la información de vuelos...')
def transform_flights():
    
    flights = pd.DataFrame(st.session_state[FLIGHTS])
    
    # Change Type of numeric columns
    flights[flight_columns_numeric] = (
        flights[flight_columns_numeric]
        .replace(',', '.', regex=True)
        .apply(pd.to_numeric)
    )

    flights['departure_date'] = pd.to_datetime(flights['departure_date'])
    flights['model'] = flights['model'].str.strip()
    
    # Map airlines names
    dictionary_airlines = dict(pd.DataFrame(st.session_state[AIRLINES], columns=['airlineCode', 'airlineName']).values)
    flights['airlineName'] = flights['airlineCode'].map(dictionary_airlines)
    flights['airlineName'] = flights['airlineName'].str.strip()
    
    # Map Airport names
    dictionary_airports = dict(pd.DataFrame(st.session_state[AIRPORTS], columns=['code', 'name']).values)
    flights['departureAirportName'] = flights['departureAirportCode'].map(dictionary_airports)
    flights['arrivalAirportName'] = flights['arrivalAirportCode'].map(dictionary_airports)
    
    # Map Cities
    airports_cities = pd.DataFrame(st.session_state[AIRPORTS], columns=['code', 'city'])
    airports_cities['city'] = airports_cities['city'].str.strip()
    
    dictionary_cities = dict(airports_cities.values)
    flights['departureCity'] = flights['departureAirportCode'].map(dictionary_cities)
    
    return flights


def apply_filters() -> pd.DataFrame:
    
    # Cached data
    flights = transform_flights()
    
    selected_city = st.session_state[CITY_SELECTED]
    selected_airline = st.session_state[AIRLINE_SELECTED]
    selected_model = st.session_state[MODEL_SELECTED]
    max_selected_price = st.session_state[MAX_PRICE_SELECTED]
    date1_selected = st.session_state[DATE1_SELECTED]
    date2_selected = st.session_state[DATE2_SELECTED]

    date1_selected = pd.to_datetime(date1_selected)
    date2_selected = pd.to_datetime(date2_selected)
    
    # Build combined mask
    mask = pd.Series(True, index=flights.index)
    
    # City filter
    if selected_city != "Todas":
        mask &= (flights["departureCity"] == selected_city)
    
    # Airline filter
    if selected_airline != "Todas":
        mask &= (flights["airlineName"] == selected_airline)
    
    # Model filter
    if selected_model != "Todos":
        mask &= (flights["model"] == selected_model)
    
    # Price filter
    mask &= (flights["totalFare"] <= max_selected_price)
    
    # Date filter
    if date2_selected < date1_selected:
        st.toast('La segunda Fecha de Salida no puede ser anterior que la primera. No será tenida en cuenta para el filtrado', icon='⚠️')
        mask &= (flights['departure_date'] >= date1_selected)
    else:
        mask &= (flights['departure_date'] >= date1_selected) & (flights['departure_date'] <= date2_selected)
    
    return flights[mask].copy()