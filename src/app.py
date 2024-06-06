import os
import pandas as pd
import dash
from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go

from src.wordcloud_builder import create_a_wordcloud, wordcloud_to_plotly
from src.paper_widget import generate_paper_list
from src.barplot_widget import update_bar_plot
from src.utils import create_tag_to_organizations_map, create_organization_to_tags_map, create_list_of_papers_from_tags_and_orgs
from src.layout import create_default_layout
from src.config import create_config

app = Dash(__name__, suppress_callback_exceptions=True,)
server = app.server

def load_data(data_dir, data_csv: str):
    data_path = os.path.join(data_dir, data_csv)
    data = pd.read_csv(data_path)
    data = data[['title', 'authors', 'institutes', 'abstract', 'project_link', 'paper_link', 'relevant_tags', 'novelty_rating', 'impact_rating']]
    return data

cfg = create_config()
data = load_data(cfg.DATA_DIR, cfg.DATA_CSV)


######################## INITIALIZE WIDGETS ########################

tag_wordcloud, tags, tag_word_data = create_a_wordcloud(data, cfg.RELEVANT_TAGS)
tag_fig_wc = wordcloud_to_plotly(tag_word_data)
org_wordcloud, orgs, org_word_data = create_a_wordcloud(data, cfg.RELEVANT_ORGS)
org_fig_wc = wordcloud_to_plotly(org_word_data)

tag_to_org_map = create_tag_to_organizations_map(data, valid_tags=tag_wordcloud.words_.keys())
org_to_tag_map = create_organization_to_tags_map(data, valid_orgs=org_wordcloud.words_.keys())
fig_bar_tag = update_bar_plot(tag_based=True, search_words=['generative models'], key_to_paper_map=tag_to_org_map)
fig_bar_org = update_bar_plot(tag_based=False, search_words=['Google'], key_to_paper_map=org_to_tag_map)

app.layout = create_default_layout(cfg, tag_fig_wc, tags)

######################## APP CALLBACKS ########################

@app.callback(
    Output('wordcloud', 'figure'),
    Output('word-dropdown', 'options'),
    Output('word-dropdown', 'placeholder'),
    Output('selected-bar', 'children', ),
    Output('active-tags', 'data'),
    Output('active-orgs', 'data'),
    Input('cloud-type', 'value'),
)
def switch_wordcloud(cloud_type):
    """
    Switch between tags and organizations wordclouds by a radio button
    """
    active_orgs = []
    active_tags = []
    selected_words_placeholder = ''
    selected_bar_placeholder = ''
    if cloud_type == 'tags':
        wordcloud, tags, word_data = create_a_wordcloud(data, cfg.RELEVANT_TAGS)
        fig_wc = wordcloud_to_plotly(word_data)
        options = [{'label': tag, 'value': tag} for tag in tags]
        selected_words_placeholder = 'Click Wordcloud or Select tags...'
        selected_bar_placeholder = 'Selected Tags: None'
    else:
        wordcloud, orgs, org_data = create_a_wordcloud(data, cfg.RELEVANT_ORGS)
        fig_wc = wordcloud_to_plotly(org_data)
        options = [{'label': org, 'value': org} for org in orgs]
        selected_words_placeholder = 'Click Wordcloud or Select organizations...'
        selected_bar_placeholder = 'Selected Organizations: None'
    return fig_wc, options, selected_words_placeholder, selected_bar_placeholder, active_tags, active_orgs


@app.callback(
    Output('word-dropdown', 'value'),
    Output('selected-words', 'children'),
    Output('bar-container', 'children', allow_duplicate=True),
    Output('active-tags', 'data', allow_duplicate=True),
    Output('active-orgs', 'data', allow_duplicate=True),
    Input('wordcloud', 'clickData'),
    State('word-dropdown', 'value'),
    State('active-tags', 'data'),
    State('active-orgs', 'data'),
    State('cloud-type', 'value'),
    prevent_initial_call=True
)
def upon_wordcloud_click(click_data, current_words, active_tags, active_orgs, cloud_type):
    """
    Update the dropdown & bar with the clicked word
    """
    if current_words is None:
        current_words = []

    clicked_word = None
    if click_data is not None:
        clicked_word = click_data['points'][0]['text']
        if clicked_word not in current_words:
            current_words.append(clicked_word)

    display = 'Selected: None'
    fig_bar = {}

    if cloud_type == 'tags':
        active_tags = current_words
        fig_bar = update_bar_plot(tag_based=True, search_words=active_tags, key_to_paper_map=tag_to_org_map)
        display = "Selected Tags: " + ", ".join(active_tags) if active_tags else "Selected Tags: None"
    elif cloud_type == 'orgs':
        active_orgs = current_words
        fig_bar = update_bar_plot(tag_based=False, search_words=active_orgs, key_to_paper_map=org_to_tag_map)
        display = "Selected Orgs: " + ", ".join(active_orgs) if active_orgs else "Selected Orgs: None"
    return current_words, display, fig_bar, active_tags, active_orgs
    

@app.callback(
    Output('paper-container', 'children'),
    Output('selected-bar', 'children', allow_duplicate=True),
    Output('active-tags', 'data', allow_duplicate=True),
    Output('active-orgs', 'data', allow_duplicate=True),
    Input('bar-plot', 'clickData'),
    State('active-tags', 'data'),
    State('active-orgs', 'data'),
    State('cloud-type', 'value'),
    prevent_initial_call=True
)
def upon_barplot_element_click(click_data, active_tags, active_orgs, cloud_type):
    clicked_bar_element = None
    if click_data is not None:
        clicked_bar_element = click_data['points'][0]['y']
    
    selected_bar_element_display = f"Selected: {clicked_bar_element}" if clicked_bar_element else "Selected: None"
    if cloud_type == 'tags':
        active_orgs = [clicked_bar_element] if clicked_bar_element else []
    elif cloud_type == 'orgs':
        active_tags = [clicked_bar_element] if clicked_bar_element else []
    
    if active_tags and active_orgs:
        papers = create_list_of_papers_from_tags_and_orgs(data, active_tags, active_orgs)
        paper_list = generate_paper_list(papers)
    else:
        paper_list = generate_paper_list([])
    return paper_list, selected_bar_element_display, active_tags, active_orgs


@app.callback(
    Output('selected-words', 'children', allow_duplicate=True),
    Output('selected-bar', 'children', allow_duplicate=True),
    Output('active-tags', 'data', allow_duplicate=True),
    Output('active-orgs', 'data', allow_duplicate=True),
    Output('bar-container', 'children', allow_duplicate=True),
    Output('paper-container', 'children', allow_duplicate=True),
    Input('word-dropdown', 'value'),
    State('active-tags', 'data'),
    State('active-orgs', 'data'),
    State('cloud-type', 'value'),
    prevent_initial_call=True
)
def upon_search_bar_update(selected_words, active_tags, active_orgs, cloud_type):
    if selected_words is None:
        selected_words = []

    selected_words_display = 'Selected: None'
    selected_bar_display = 'Selected: None'
    fig_bar = {}
    if cloud_type == 'tags':
        active_tags = selected_words
        selected_words_display = "Selected Tags: " + ", ".join(active_tags) if active_tags else "Selected Tags: None"
        selected_bar_display = "Selected Organizations: None"
        active_orgs = []
        fig_bar = update_bar_plot(tag_based=True, search_words=active_tags, key_to_paper_map=tag_to_org_map)
    elif cloud_type == 'orgs':
        active_orgs = selected_words
        selected_words_display = "Selected Orgs: " + ", ".join(active_orgs) if active_orgs else "Selected Orgs: None"
        selected_bar_display = "Selected Tags: None"
        active_tags = []
        fig_bar = update_bar_plot(tag_based=False, search_words=active_orgs, key_to_paper_map=org_to_tag_map)
    return selected_words_display, selected_bar_display, active_tags, active_orgs, fig_bar, generate_paper_list([])

    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)
