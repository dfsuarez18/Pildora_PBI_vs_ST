import streamlit as st
from utils.global_conf import *
from pages.st_top_navbar import *
import plotly.express as px
import folium
from streamlit_folium import folium_static
import pandas as pd


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

flights = pd.DataFrame(st.session_state[FLIGHTS])
flight_columns_exclude = list(flights.columns)

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
distance_col = pd.DataFrame(st.session_state[FLIGHTS])['distance_km']
price_col = pd.DataFrame(st.session_state[FLIGHTS])['totalFare']

total_distance = pd.to_numeric(distance_col, errors='coerce').sum(skipna=True)
total_price = pd.to_numeric(price_col, errors='coerce').sum(skipna=True)
total_flights = len(flights)


########### Filtros ##############

colfilt1, colfilt2, colfilt3 = st.columns(3)

# Asegurarse de que los valores son strings y no hay nulos
flights["departureAirportName"] = flights["departureAirportName"].fillna("Desconocido").astype(str)
flights["airlineName"] = flights["airlineName"].fillna("Desconocido").astype(str)
flights["model"] = flights["model"].fillna("Desconocido").astype(str)

# Crear listas únicas sin errores
ciudades = flights["departureAirportName"].unique()
aerolineas = flights["airlineName"].unique()
modelos = flights["model"].unique()

# Widgets seguros
ciudad_sel = colfilt1.selectbox("Ciudad de salida", ["Todas"] + sorted(ciudades))
aerolinea_sel = colfilt2.selectbox("Aerolínea", ["Todas"] + sorted(aerolineas))
modelo_sel = colfilt3.selectbox("Modelo de avión", ["Todas"] + sorted(modelos))

# Aplicar filtros
df_filtrado = flights.copy()
if ciudad_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["departureAirportName"] == ciudad_sel]
if aerolinea_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["airlineName"] == aerolinea_sel]
if modelo_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["model"] == modelo_sel]

colgraph1, colgraph2 = st.columns(2)

vuelos_por_aerolinea = df_filtrado['airlineName'].value_counts().reset_index()
vuelos_por_aerolinea.columns = ['airlineName', 'Número de vuelos']

# Gráfica de barras
fig = px.bar(
    vuelos_por_aerolinea.sort_values('Número de vuelos', ascending=True),
    x='Número de vuelos',
    y='airlineName',
    orientation='h',
    title='Número de vuelos por Aerolínea',
    text='Número de vuelos'
)

fig.update_layout(
    yaxis_title='Aerolínea',
    xaxis_title='Número de vuelos',
    height=600  # Incrementar la altura del gráfico
)
fig.update_traces(texttemplate='%{text:.3s}', textposition='outside')


colgraph1.plotly_chart(fig, use_container_width=True)



df_filtrado['departureAirportCode'] = df_filtrado['departureAirportCode'].str.strip()

# Conteo de salidas por aeropuerto
salidas = df_filtrado.groupby('departureAirportCode').size().reset_index(name='Número de salidas')

# Diccionario con coordenadas de ejemplo
coordenadas = {
    "LAX": (33.9416, -118.4085),
    "ORD": (41.9742, -87.9073),
    "ATL": (33.6407, -84.4277),
    "BOS": (42.3656, -71.0096),
    "SFO": (37.6213, -122.3790),
    "CLT": (35.2140, -80.9431),
    "EWR": (40.6895, -74.1745),
    "MIA": (25.7959, -80.2870),
    "DFW": (32.8998, -97.0403),
    "LGA": (40.7769, -73.8740),
    "JFK": (40.6413, -73.7781),
    "DAL": (32.8471, -96.8517),
    "DTW": (42.2162, -83.3554),
    "PHL": (39.8744, -75.2424),
    # Añade más si hace falta
}

# Añadir columnas de lat y lon
salidas['lat'] = salidas['departureAirportCode'].map(lambda x: coordenadas.get(x, (None, None))[0])
salidas['lon'] = salidas['departureAirportCode'].map(lambda x: coordenadas.get(x, (None, None))[1])
salidas = salidas.dropna(subset=['lat', 'lon'])

# Crear el mapa base centrado en EE.UU.
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Añadir marcadores como burbujas
for _, row in salidas.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['Número de salidas'] / 5000,  # Ajusta según tus datos
        popup=f"{row['departureAirportCode']}: {row['Número de salidas']} salidas",
        color='blue',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

# Mostrar el mapa en Streamlit
with colgraph2:
    st.write("")
    st.markdown("**Mapa de salidas por aeropuerto**")
    folium_static(m)

# Gráfico donut
data = {
    "Modelo": [
        "AIRBUS A321", "BOEING 737-800", "BOEING 737-900", "AIRBUS A320",
        "AIRBUS A319", "EMBRAER 175 (ENHANCED)", "EMBRAER 190", "BOEING 757-200",
        "AIRBUS A330", "BOEING 767-300"
    ],
    "Kilometraje": [
        314.8, 302.35, 215.44, 143.82, 97.12, 58.69, 53.99, 45.8, 38.4, 33.5
    ]
}

df = pd.DataFrame(data)

# Crear gráfico donut
fig = px.pie(
    df,
    names="Modelo",
    values="Kilometraje",
    hole=0.5,
    title="Top 10 Modelos con más Kilometraje"
)

fig.update_traces(textinfo='percent+value', textposition='outside')
fig.update_layout(showlegend=True, height=500)

# Mostrar en Streamlit
colgraph1.plotly_chart(fig, use_container_width=True)