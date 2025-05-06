import streamlit as st
import pandas as pd
import numpy as np
import logging as log

from utils.file_functions import *
from utils.global_conf import *
from pages.st_top_navbar import show_filters

# Page Configuration
PAGE_SUMMARY = st.Page("./pages/st_summary.py", title="Graphic Summary of Flights", icon='📊')
PAGE_DETAIL = st.Page("./pages/st_details.py", title="Flight Details", icon='ℹ️')
PAGE_EXTRAS = st.Page("./pages/st_extras.py", title="Extra Graphs", icon='🎁')
PAGE_LIST = [PAGE_SUMMARY, PAGE_DETAIL]

def column_to_list(df: pd.DataFrame, column_name: str):
    processed_serie = pd.Series(df[column_name].dropna(axis=0).to_numpy()).str.strip().sort_values().unique()
    return processed_serie.tolist()

@st.cache_resource(show_spinner=False)
def truncate_log_file(max_lines=800, lines_to_leave=600):

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if(len(lines) > max_lines):
            with open(LOG_PATH, 'w', encoding='utf-8') as file:
                file.writelines(lines[-lines_to_leave:])

@st.cache_resource(show_spinner=False)
def conf_log():
    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            log.FileHandler(LOG_PATH, mode='a', encoding='utf-8'),
            log.StreamHandler()
        ]
    )

def validate_initial_data(cached_value):
    for table in TABLE_LIST:
        if table not in st.session_state:
            return False
    return True

@st.cache_resource(validate=validate_initial_data, show_spinner="Cargando la información de vuelos desde los ficheros locales...")
def load_data():
    for i in range(len(TABLE_LIST)):
        path = CSV_LIST[i]
        name = TABLE_LIST[i]

        st.session_state[name] = read_csv(path)
        
    # Configure filter data
    st.session_state[LIST_CITIES] = column_to_list(st.session_state[AIRPORTS], 'city')
    st.session_state[LIST_AIRLINES] = column_to_list(st.session_state[AIRLINES], 'airlineName')
    st.session_state[LIST_MODELS] = column_to_list(st.session_state[AIRPLANES], 'model')
    
    price_array = pd.Series(st.session_state[FLIGHTS]['totalFare']).dropna(axis=0)
    st.session_state[MAX_PRICE] = int(price_array.max())
    st.session_state[MIN_PRICE] = int(price_array.min())
    
    departure_date_col = pd.to_datetime(
        pd.Series(st.session_state[FLIGHTS]['departure_date']).dropna()
    )
    st.session_state[MAX_DEPARTURE_DATE] = departure_date_col.max()
    st.session_state[MIN_DEPARTURE_DATE] = departure_date_col.min()
    
    st.session_state[CITY_SELECTED] = 'Todas'
    st.session_state[AIRLINE_SELECTED] = 'Todas'
    st.session_state[MODEL_SELECTED] = 'Todos'
    st.session_state[MAX_PRICE_SELECTED] = st.session_state[MAX_PRICE]
    st.session_state[DATE1_SELECTED] = st.session_state[MIN_DEPARTURE_DATE]
    st.session_state[DATE2_SELECTED] = st.session_state[MAX_DEPARTURE_DATE]

st.set_page_config(
    page_title="NTT Air Dashboard",
    page_icon="✈️",
    layout="wide",
    
    initial_sidebar_state='collapsed')

truncate_log_file()
conf_log()
load_data()

pg = st.navigation(PAGE_LIST)
pg.run()