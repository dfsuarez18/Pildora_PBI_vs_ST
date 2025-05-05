import folium
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging as log

__logger = log.getLogger('app.utils.graph_functions')


def horizontal_bars_graph(title: str, x_axis_title: str, y_axis_title: str, data: pd.DataFrame, bar_color: str):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: x_axis_title, column1: y_axis_title}

    fig = px.bar(data, x=column0, y=column1, title=title, labels=labels, color_discrete_sequence=[bar_color])

    return fig

def pie_chart(title: str, names_title: str, values_title: str, data: pd.DataFrame, color_list: list):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: names_title, column1: values_title}

    fig = px.pie(data, title=title, names=column0, values=column1, labels=labels, color=column0, 
                 color_discrete_sequence=color_list)

    return fig

def line_graph_with_avg(title: str, x_axis_title: str, y_axis_title: str, avg_title: str, data: pd.DataFrame, avg: float, 
                        primary_line_color: str, horizontal_line_color: str):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: x_axis_title, column1: y_axis_title}
    
    fig = px.line(data, x=column0, y=column1, labels=labels, title=title, color_discrete_sequence=[primary_line_color])
    
    fig.add_hline(y=avg, line_dash="dash", line_color=horizontal_line_color, 
        annotation_text=f"{avg_title}: {avg:.2f}", 
        annotation_position="bottom right")

    return fig

def bubble_chart_map(hoover_info: dict, size_col: str, latitude_col: str, longitude_col: str, data: pd.DataFrame, bubble_color: str):
    
    # Creates the base map, centered in EEUU
    fig = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
    
    # Adds the bubbles for each row
    for _, row in data.iterrows():
        
        # Creates the popup msg:
        popup_content = '<div style="width: 150px;">'
        popup_content += '<br>'.join(f"<b>{key}:</b> {row[value]}" for key, value in hoover_info.items())
        popup_content += '</div>'
        
        folium.CircleMarker(
            location=[row[latitude_col], row[longitude_col]],
            radius=row[size_col] / 5000,
            popup=folium.Popup(popup_content, max_width=300),
            color=bubble_color,
            fill=True,
            fill_opacity=0.6
        ).add_to(fig)
    
    return fig

def bubble_chart_map_colors(title: str, color_col: str, hoover_col: str, size_col: str, latitude_col: str, longitude_col: str, 
                            data: pd.DataFrame, color_list: list, scope: str = 'usa'):
    
    fig = px.scatter_geo(
        data, title=title, lat=latitude_col, lon=longitude_col, color=color_col, 
        hover_name=hoover_col, size=size_col, projection="albers usa", scope=scope, 
        basemap_visible=True, color_discrete_sequence=color_list
    )
    
    return fig