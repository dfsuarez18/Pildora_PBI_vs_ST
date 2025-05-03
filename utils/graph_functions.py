import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging as log

__logger = log.getLogger('app.utils.graph_functions')


def horizontal_bars_graph(title: str, x_axis_title: str, y_axis_title: str, data: pd.DataFrame):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: x_axis_title, column1: y_axis_title}

    fig = px.bar(data, x=column0, y=column1, title=title, labels=labels, color_continuous_scale='Blues')

    return fig

def pie_chart(title: str, names_title: str, values_title: str, data: pd.DataFrame, color_discrete_map = None):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: names_title, column1: values_title}

    if color_discrete_map is None:
        fig = px.pie(data, title=title, names=column0, values=column1, labels=labels)
    else:
        fig = px.pie(data, title=title, names=column0, values=column1, labels=labels, color=column0, color_discrete_map=color_discrete_map)

    return fig

def line_graph_with_avg(title: str, x_axis_title: str, y_axis_title: str, avg_title: str, data: pd.DataFrame, avg: float):

    column0 = data.columns[0]
    column1 = data.columns[1]

    labels = {column0: x_axis_title, column1: y_axis_title}
    
    fig = px.line(data, x=column0, y=column1, labels=labels, title=title)
    
    fig.add_hline(y=avg, line_dash="dash", line_color="blue", 
        annotation_text=f"{avg_title}: {avg:.2f}", 
        annotation_position="bottom right")

    return fig

def buble_chart_map(title: str, color_col: str, hoover_col: str, size_col: str, latitude_col: str, longitude_col: str, data: pd.DataFrame, scope: str = 'usa'):
    
    fig = px.scatter_geo(
        data, title=title, lat=latitude_col, lon=longitude_col, color=color_col, 
        hover_name=hoover_col, size=size_col, projection="albers usa", scope=scope, 
        basemap_visible=True, color_discrete_sequence=px.colors.qualitative.Prism
    )
    
    return fig