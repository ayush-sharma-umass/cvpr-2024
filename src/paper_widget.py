import dash
from dash import dcc, html

from src.config import create_config

cfg = create_config()

def generate_paper_table(paper):
    table = html.Table(
        className="paper-table",
        children=[
            html.Tr([
                html.Th("Title"), 
                html.Td(html.B(paper['title']), style={"font-size": "1.2em"}, className="title-cell")
            ], style={"background-color": "#f2f2f2", 
                      "font-family": "Helvetica",
                      "padding": "10"}),  
            html.Tr([
                html.Th("Authors"), 
                html.Td(paper['authors'])
            ], style={"background-color": "#e6e6e6", 
                      "font-family": "Arial, sans-serif",
                      "padding": "10"}),  
            html.Tr([
                html.Th("Abstract"), 
                html.Td(paper['abstract'])  # Increase font size of abstract
            ], style={"background-color": "#f2f2f2", 
                      "font-family": "Arial, sans-serif",
                      "padding": "10"}),  
            html.Tr([
                html.Th("Tags"), 
                html.Td(paper['relevant_tags'])  # Increase font size of abstract
            ], style={"background-color": "#f2f2f2", 
                      "font-family": "Arial, sans-serif",
                      "padding": "10"}),  
            html.Tr([
                html.Th("Paper Link"), 
                html.Td(html.A("link", href=paper['paper_link']))
            ], style={"background-color": "#e6e6e6", 
                      "font-family": "Arial, sans-serif",
                      "padding": "10"})  # 
        ],
        style={'overflow-y':'auto', 
                  'height':300, 
                  'width': 800, 
                  'background-color': '#f0f0f0', 
                  'padding': '0px',
                  }
    )
    return table

def generate_paper_list(papers):
    paper_list = []
    for i, paper in enumerate(papers):
        paper_list.append(
            html.Div(
                className="paper-entry",
                style={"border": "1px solid black" if i % 2 == 0 else "1px solid blue",
                       "width": "800px",  # Set width of each paper entry
                       "padding": "10px"},  # Add padding around each paper entry
                children=generate_paper_table(paper)
            )
        )
    return paper_list



