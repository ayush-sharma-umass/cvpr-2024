import pandas as pd
import dash
from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go

from src.wordcloud_builder import wordcloud_to_plotly
from src.paper_widget import generate_paper_list
from src.sidebar_widgets import create_instruction_box, create_radio_buttons, create_explanation_box
from src.markdown_consts import markdown_library


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
                html.Div(
                    children=[
                        html.A(
                            children=[
                                html.Img(src='././static/LI-In-Bug.png', style={
                                    'width': '40px',
                                    'height': '40px',
                                    'verticalAlign': 'middle'
                                }),
                                html.Span('Ayush Sharma', style={'marginLeft': '2px', 'color': '#000000'})
                            ],
                            href='https://www.linkedin.com/in/ayushsharma-umass/',
                            target='_blank',
                            style={
                                'textDecoration': 'none',
                                'color': '#ffffff',
                                'display': 'flex',
                                'alignItems': 'center'
                            }
                        )
                    ],
                    style={
                        'position': 'absolute',
                        'bottom': '10px',
                        'right': '10px',
                        'backgroundColor': '#DADBDD',
                        'padding': '10px',
                        'border': '2px solid #ffffff',
                        'borderRadius': '5px'
                    }
                )
            ],
            style={
                'backgroundColor': '#527A35',  # Replace with your desired color
                'padding': '20px',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'border': '2px solid #ffffff',
                'position': 'relative'
            }
        ),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row'},
            children=[
                # Left sidebar with centered radio buttons and colored panel
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
                        create_radio_buttons(uid='cloud-type',
                                             options=["Tags", "Organizations"], 
                                             selected="Tags", 
                                             header="Select Wordcloud Type"),
                        html.Div(id='wordcloud-desc', children=create_explanation_box(markdown_text=markdown_library[cfg.TAGS_EXPLANATION])),
                        
                    ]
                ),
                # Content area with the same styles
                html.Div(
                    className="content",
                    style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top'},
                    children=[
                        dcc.Graph(id='wordcloud', figure=fig_wc, style={'width': '80%'}),
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
                                'width': '80%',
                                'padding': 20,
                                'backgroundColor': '#ffffff',
                                'border': '1px solid #d3d3d3'},
                            children=generate_paper_list([])
                        ),
                        dcc.Store(id='active-tags', data=[]),
                        dcc.Store(id='active-orgs', data=[])
                    ]
                ),
                # Right sidebar with blue colored boxes
                html.Div(
                    className="right-sidebar",
                    style={
                        'width': '20%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '20px',
                        'backgroundColor': '#93C572'  # Match left sidebar color
                    },
                    children=[
                        # Stack three blue boxes with padding
                        create_instruction_box("Step 1", "Click on the wordcloud to select words or type in the search bar. \nYou can select multiple tags!"),
                        create_instruction_box("Step 2", "Click on the bar plot to view papers below."),
                        create_instruction_box("Step 3", "Scroll down below to see list of papers!"),
                    ],
                )
            ]
        )
    ])
