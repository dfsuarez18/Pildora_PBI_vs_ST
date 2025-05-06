import streamlit as st
import plotly.colors
from utils.global_conf import *

# -----------------------------Color Configuration---------------------------------

PRIMARY_COLOR = st.get_option("theme.primaryColor")
SECONDARY_COLOR = "#1e81b0"
GRAPH_COLOR_LIST = [PRIMARY_COLOR] + plotly.colors.qualitative.Prism[:-1] + plotly.colors.qualitative.Pastel[:-1]

# -----------------------------Logo Configuration----------------------------------
def show_logo():    
    _, col, _ = st.columns([0.4, 0.2, 0.4])
    
    col.image(TOP_IMAGE)

# -----------------------------Filter Components Configuration---------------------------

def show_filters():
    
    with st.container(height=130, border=True):

        col_filter1, col_filter2, col_filter3, col_filter4, col_filter5 = st.columns(5)

        st.session_state[MAX_PRICE_SELECTED] = col_filter1.slider("Máximo precio del billete", st.session_state[MIN_PRICE], 
                                                                st.session_state[MAX_PRICE], value=st.session_state[MAX_PRICE], step=1)

        st.session_state[CITY_SELECTED] = col_filter2.selectbox("Ciudad de Salida", ["Todas"] + st.session_state[LIST_CITIES])
        st.session_state[AIRLINE_SELECTED] = col_filter3.selectbox("Aerolínea", ["Todas"] + st.session_state[LIST_AIRLINES])
        st.session_state[MODEL_SELECTED] = col_filter4.selectbox("Modelo de Avión", ["Todos"] + st.session_state[LIST_MODELS])

        date1, date2 = col_filter5.columns(2)
            
        st.session_state[DATE1_SELECTED] = date1.date_input(
            "Fecha de salida", 
            value=st.session_state[MIN_DEPARTURE_DATE], 
            min_value=st.session_state[MIN_DEPARTURE_DATE], 
            max_value=st.session_state[MAX_DEPARTURE_DATE]
        )

        st.session_state[DATE2_SELECTED] = date2.date_input(
            "date2", 
            value=st.session_state[MAX_DEPARTURE_DATE],
            min_value=st.session_state[MIN_DEPARTURE_DATE],
            max_value=st.session_state[MAX_DEPARTURE_DATE], 
            label_visibility='hidden',
            key='filter_date2'
        )