import streamlit as st
import pandas as pd
import logging as log

from utils.file_functions import *
from utils.global_conf import *

# Page Configuration
PAGE_SUMMARY = st.Page("./pages/st_summary.py", title="Graphic Summary of Flights", icon='📊')
PAGE_DETAIL = st.Page("./pages/st_details.py", title="Flight Details", icon='ℹ️')
PAGE_LIST = [PAGE_SUMMARY, PAGE_DETAIL]

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
        level=log.DEBUG,
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

st.set_page_config(
    page_title="NTT Air Dashboard",
    page_icon="✈️",
    layout="wide",
    
    initial_sidebar_state='expanded')

truncate_log_file()
conf_log()
load_data()

pg = st.navigation(PAGE_LIST)
pg.run()