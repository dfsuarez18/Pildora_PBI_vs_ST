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

def apply_filters():
    
    flights = pd.DataFrame(st.session_state[FLIGHTS])
    
    # Change Type of numeric columns
    flights[flight_columns_numeric] = (
        flights[flight_columns_numeric]
        .replace(',', '.', regex=True)
        .apply(pd.to_numeric)
    )

    flights[['departure_date']] = flights[['departure_date']].apply(pd.to_datetime)
    
    # Map airlines names
    dictionary_airlines = dict(pd.DataFrame(st.session_state[AIRLINES], columns=['airlineCode', 'airlineName']).values)
    flights['airlineName'] = flights['airlineCode'].map(dictionary_airlines)
    
    # Map Airport names
    dictionary_airports = dict(pd.DataFrame(st.session_state[AIRPORTS], columns=['code', 'name']).values)
    flights['departureAirportName'] = flights['departureAirportCode'].map(dictionary_airports)
    flights['arrivalAirportName'] = flights['arrivalAirportCode'].map(dictionary_airports)
    
    #TODO: Apply the filters
    
    return flights