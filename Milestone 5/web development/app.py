import json
import base64
import datetime 
import requests
import pathlib
import math
import pandas as pd
import flask
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table as dt

from dash.dependencies import Input, Output, State
from plotly import tools
from collections import OrderedDict

from datetime import date, timedelta
import time

from tests import web_scraper

from predictiontest import update_prediction

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.config['suppress_callback_exceptions'] = True

server = app.server

# Currency pairs
currencies = ["bitcoin", "ethereum", "litecoin"]

# API Requests for news div
news_requests = requests.get(
    "http://newsapi.org/v2/everything?q=bitcoin&sortBy=publishedAt&apiKey=65fd7860d9894f7bb465371384f9799b",
     headers = {'User-Agent' : 'Chrome/74.0.3729.169'}
)
   

# API Call to update news
def update_news():
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 10
    return html.Div(
        children=[
            html.P(className="p-news", children="Headlines"),
            html.P(
                className="p-news float-right",
                children="Last update : "
                + datetime.datetime.now().strftime("%H:%M:%S"),
            ),
            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ],
            ),
        ]
    )

# returns chart div
def chart_div():
    return html.Div(
        #id="graph_div",
        className="display",
        children=[
            # Menu for Currency Graph
                    # stores current menu tab    
                    # Styles checklist
            # Chart Top Bar
                    # Dropdown and close button float right
            html.Div(
                dcc.Graph(
                    id="live-chart",
                    className="chart-graph",
                    config={"displayModeBar": False, "scrollZoom": True},
                )
            ),
        ],
    )

# MAIN CHART TRACES (STYLE list)
def line_trace(df):
    trace = go.Scatter(
        x=df.index, y=df["Close"], mode="lines", showlegend=False, name="line"
    )
    return trace

def candlestick_trace(df):
    return go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing=dict(line=dict(color="#00ff00")),
        decreasing=dict(line=dict(color="#FF2400")),
        showlegend=False,
        name="candlestick",
    )

def web_scrap(value):
    data_frame = web_scraper(value).reset_index(drop=True).set_index('Date').sort_index()
    data_frame.index = pd.to_datetime(data_frame.index)
    t = datetime.datetime.now()
    # all the data from the beginning until current time
    data = data_frame.loc["2016-10-15"
        : t.strftime(
        "%Y%m%d" #"2020-06-10"# %H:%M:%S"
        )
    ]
    return data

# Dash App Layout
app.layout = html.Div(
    className="row",
    children=[
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
        # Interval component for ask bid updates
        #dcc.Interval(id="i_bis", interval=1 * 2000, n_intervals=0),
        # Interval component for graph updates
        dcc.Interval(id="i_tris", interval=1 * 50000, n_intervals=0),
        # Interval component for graph updates
        dcc.Interval(id="i_news", interval=1 * 60000, n_intervals=0),
        # Left Panel Div
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("logo.jpeg")
                        ),
                        html.H3("Crypto App"),
                        html.P(
                            """
                            This app presents some news information regarding the cryptocurrencies, as welll as the prices.
                            
                            DISCLAIMER: The app is just for scientific knowledge, the predicting price can be misleading. 
                            """
                        ),
                    ],
                ),
                # Div for News Headlines
                html.Div(
                    className="div-news",
                    children=[html.Div(id="news", children=update_news())],
                ),
            ],
        ),
        # Right Panel Div
        html.Div(
            className="nine columns div-right-panel",
            children=[
                html.Div(
                    html.Div(
                    html.H1("Cryptocurrecy prices movement in visualisation")
                ),
                style={'margin-top': '1vh', 'color': '#98AFC7'}
                ),
                # Top Bar Div - To chose the cyptocurrecy
                html.Div(
                    #className="inline-block",
                    children=[
                        dcc.Dropdown(
                            className="coin-dropdown",
                            id="coin-dropdown",   
                            options=[
                                { "label": "Bitcoin" , "value": "bitcoin",},
                                { "label": "Ethereum", "value": "ethereum"},
                                { "label": "Litecoin", "value": "litecoin"},
                            ],
                            value='bitcoin',
                            style={'width': '100%', 'display': 'inline-block'}
                        ),                        
                    ],
                ),
                # Charts Div
                html.Div(
                    id="charts",
                    className="row",
                    children=[html.Div(id="graph", children=chart_div())],
                ),
                # Period option
                html.Div([
                    html.P("Period"),
                    dcc.Dropdown(
                        id="period",
                        options=[
                            { "label": '1 day', "value": "1D"},
                            { "label": '10 day', "value": "10D"},
                            { "label": '2 Month', "value": "2m"},
                            { "label": '6 Month', "value": "6m"},
                        ],
                        value="1D"
                    )
                ],style={'width': '40%', 'display': 'inline-block'}),
                # Style option
                html.Div([
                    html.P("Styles"),
                    dcc.Dropdown(
                        id="Style_list",
                        options=[
                            { "label": 'Line', "value": "line_trace"},
                            { "label": 'candlestick', "value": "candlestick_trace"},
                        ],
                        value="line_trace"
                    ),
                ],style={'width': '40%', 'margin-left': '10%', 'display': 'inline-block'}),
                # Panel for prediction
                html.Div(
                    html.Div(
                    id="predict_process"
                    ),style={'margin-top': '3vh', 'margin-bottom': '2vh'}
                ),
                html.Div(
                    children=[
                        html.Div(html.P('History Data Table'), style={ 'margin-left': '1%'}),
                        html.Div(
                            id='table'
                            )
                        ]
                    )
            ]
        )
    ]
)


@app.callback(
    Output("table", "children"),
    [
        Input("coin-dropdown", "value")
    ]
)
def update_table(value):
    data = web_scrap(value)
    data = data[-180:]
    data= data.reset_index('Date')
    return  html.Div(
        dt.DataTable(
            id='table_box',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('record'),
            editable=True,
            row_deletable=True,
            page_action="native",
            page_current= 0,
            page_size= 10,
            selected_rows=[],
            style_table={'maxHeight': '10%',
                        'width': '100%',
                        'minWidth': '0%'},
            style_header={'backgroundColor': '#ADD8E6',
                        'fontWeight': 'bold',
                        'color': 'black' },
            style_cell={'padding': '8px',
                        'whiteSpace': 'no-wrap',
                        'textOverflow': 'ellipsis',
                        'width': '550%',
                        'maxWidth': '550%',
                        'height': 50,
                        'textAlign': 'left',
                        'color': 'black',
                        'backgroundColor': '#C0C0C0'},
            style_data={'whiteSpace': 'auto','height': 'auto','width': 'auto'},
            style_cell_conditional=[],
            virtualization=True,                  
    ),style={'margin-left': '1%'}
)

@app.callback(
    Output("live-chart", "figure"),
    [
        Input("coin-dropdown", "value"),
        Input("period", "value"),
        Input("Style_list", "value"),
        Input("i_tris", "n_intervals")
    ],    
)
def update_graph(value, period, style, n):
    
    if value in currencies:
        
        data= web_scrap(value)
        df=data.resample(period).agg(
                OrderedDict([
                    ('Open','first'),
                    ('High','max'),
                    ('Low','min'),
                    ('Close','last')
                ])
        )
        
        row = 1  # number of subplots
        fig = tools.make_subplots(
        rows=row,
        shared_xaxes=True,
        shared_yaxes=True,
        cols=1,
        print_grid=False,
        vertical_spacing=0.12,
        )

        # Add main trace (style) to figure
        fig.append_trace(eval(style)(df), 1, 1)

        fig["layout"][
        "uirevision"
        ] = "The User is always right"  # Ensures zoom on graph is the same on update
        fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
        fig["layout"]["autosize"] = True
        fig["layout"]["height"] = 400
        fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
        fig["layout"]["xaxis"]["tickformat"] = "%Y-%m-%d"
        fig["layout"]["yaxis"]["showgrid"] = True
        fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
        fig["layout"]["yaxis"]["gridwidth"] = 1
        fig["layout"].update(paper_bgcolor="#21252C", plot_bgcolor="#21252C")
        
    return fig

@app.callback(
    dash.dependencies.Output('predict_process', 'children'),
    [Input("coin-dropdown", "value")], )
def update_predict(value):
    if value is not currencies:
        data = web_scrap(value)
        predict_close = update_prediction(data)
        closing_price = float(predict_close[0])
        return html.Div(
            html.H3("Predicted closing price for  " + value + " at {} is USD {:.2f} ".format(
                date.today()+ timedelta(days=1), closing_price
                    )
            ),style={'color': '#00FFFF', 'width': '90%'}
        )
        
    

# Callback to update live clock
@app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update news
@app.callback(Output("news", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()

if __name__ == "__main__":
    app.run_server(host= '127.168.0.14', port=8000, debug=True)
