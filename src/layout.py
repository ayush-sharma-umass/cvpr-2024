import pandas as pd
import dash
from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go

from src.wordcloud_builder import wordcloud_to_plotly
from src.paper_widget import generate_paper_list


def create_default_layout(cfg, fig_wc, tags):
    return html.Div([
        # Title bar with centered title and different background color
        html.Div(
            children=[
                html.H1(cfg.page_title, style={'textAlign': 'center', 
                                            "font-family": "Helvetica",
                                            "fontSize": '44px',
                                            'border': '1px solid #d3d3d3',
                                            'padding': '10px',
                                            }),
            ],
            style={
                'backgroundColor': '#527A35',  # Replace with your desired color
                'padding': '20px',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'border': '2px solid #ffffff',
            }
        ),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row'},
            children=[
                # Sidebar with centered radio buttons and colored panel
                html.Div(
                    className="sidebar",
                    style={
                        'width': '20%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '20px',
                        'border-right': '1px solid #d3d3d3',  # Separate panel from content
                        'backgroundColor': '#93C572'  # Replace with your desired side panel color
                    },
                    children=[
                        html.H3('Wordcloud Options'),
                        dcc.RadioItems(
                            id='cloud-type',
                            options=[
                                {'label': 'Tags', 'value': 'tags'},
                                {'label': 'Organizations', 'value': 'orgs'},
                            ],
                            value='tags',
                            labelStyle={'display': 'block'},
                            # Center radio buttons within sidebar
                        ),
                    ]
                ),
                # Content area with the same styles
                html.Div(
                    className="content",
                    style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'},
                    children=[
                        dcc.Graph(id='wordcloud', figure=fig_wc),
                        html.Div(id='selected-words', children="Selected Tags: None", style={'margin-bottom': '10px'}),
                        dcc.Dropdown(
                            id='word-dropdown',
                            options=[{'label': tag, 'value': tag} for tag in tags],
                            multi=True,
                            placeholder='Select or type tags...',
                            style={'width': '100%', 'margin-bottom': '20px'}
                        ),
                        html.Div(id='bar-container'),
                        html.Div(id='selected-bar', children="Selected Organization: None", style={'margin-top': '20px', 'margin-bottom': '10px'}),
                        html.Div(
                            className="paper-container",
                            id="paper-container",
                            style={"height": "900px",
                                "overflowY": "auto",
                                'width': '100%',
                                'padding': 20,
                                'backgroundColor': '#ffffff',
                                'border': '1px solid #d3d3d3'},
                            children=generate_paper_list([])
                        ),
                        dcc.Store(id='active-tags', data=[]),
                        dcc.Store(id='active-orgs', data=[])
                    ]
                )
            ]
        )
    ], style={'display': 'flex', 'flexDirection': 'column'})


