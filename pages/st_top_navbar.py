import streamlit as st
import plotly.colors
from utils.global_conf import *

# -----------------------------Color Configuration---------------------------------

PRIMARY_COLOR = st.get_option("theme.primaryColor")
SECONDARY_COLOR = "#1e81b0"
GRAPH_COLOR_LIST = [PRIMARY_COLOR] + plotly.colors.qualitative.Prism[:-1] + plotly.colors.qualitative.Pastel[:-1]

# -----------------------------Logo Configuration----------------------------------
# TODO: Insert the image in resources


# -----------------------------Filter Data Configuration---------------------------


# -----------------------------Filter Components Configuration---------------------------
# TODO: Insert the filter section
