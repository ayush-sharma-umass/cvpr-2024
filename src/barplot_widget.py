import plotly.graph_objs as go
import pandas as pd
from dash import dcc, html

from src.utils import count_papers_with_all_keys
from src.config import create_config

cfg = create_config()

def update_bar_plot(tag_based: bool, search_words: list[str], key_to_paper_map: dict) -> html.Div:
    """
    Create a bar plot for Top 25 Organizations/Tags by Paper Count
    :param tag_based: If True, the bar plot is for tags, else for organizations
    :param search_words: list of tags or organizations
    :param tag_to_org_map: dict
    :return: html.Div
    """
    if tag_based:
        xlabel='Count'
        ylabel='Organization'
        orgs_counts = count_papers_with_all_keys(key_to_paper_map, search_words)
        _df = pd.DataFrame(orgs_counts.items(), columns=[ylabel, xlabel])
    else:
        xlabel='Count'
        ylabel='Tags'
        tags_counts = count_papers_with_all_keys(key_to_paper_map, search_words)
        _df = pd.DataFrame(tags_counts.items(), columns=[ylabel, xlabel])

    _df = _df.sort_values(by=xlabel, ascending=True).tail(25)
    fig = go.Figure(
        data=[
            go.Bar(
                x=_df[xlabel],
                y=_df[ylabel],
                text=_df[xlabel],
                textposition='auto',
                width=0.8,
                marker=dict(color='skyblue'),
                orientation='h',
            )
        ],
        layout=dict(
            title='Top 25 Organizations by Paper Count',
            xaxis=dict(title=xlabel),
            yaxis=dict(tickfont=dict(size=10), title=ylabel, automargin=True),
            margin=dict(t=40, b=40, l=150, r=40),
            height=cfg.BARPLOT_HT,
            width=cfg.WORDCL_WIDTH,
            bargap=0.6
        )
    )
    fig.update_layout(template=cfg.theme)
    return html.Div(dcc.Graph(id='bar-plot', figure=fig), style={'width': cfg.WORDCL_WIDTH, 'background-color': '#FFFFFF', 'padding': '20px', 'margin-left': 20})
    # return html.Div(id='bar-container-' + id_suffix, children=[
    #     html.Div(dcc.Graph(id='bar-plot-' + id_suffix, figure=fig))
    # ], style={
    #           'width': cfg.WORDCL_WIDTH,
    #           'background-color': '#FFFFFF',
    #           'padding': '20px',
    #           'margin-left': 20})
