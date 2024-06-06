from wordcloud import WordCloud
import pandas as pd
import plotly.express as px
from collections import Counter

from src.config import create_config

cfg = create_config()

stopwords = {'a','about','above','after','again','against','ain','all','am','an','and','any','are',
 'aren',"aren't",'as','at','be','because','been','before','being','below','between','both',
 'but','by','can','couldn',"couldn't",'d','did','didn',"didn't",'do','does','doesn',"doesn't",
 'doing','don',"don't",'down','during','each','few','for','from','further','had','hadn',"hadn't",
 'has','hasn',"hasn't",'have','haven',"haven't",'having', 'her','here','hers','herself','him','himself','his',
 'how','i','if','in','into','is','isn',"isn't",'it',"it's",'its','itself','just','ll','m','ma','me','mightn', "mightn't",'more','most','mustn',"mustn't",'my','myself','needn',"needn't",'no','nor','not','now','o','of',
 'off','on','once','only','or','other','our','ours','ourselves','out','over','own','re','s','same','shan',
 "shan't",'she',"she's",'should',"should've",'shouldn',"shouldn't",'so','some','such','t','than','that',"that'll",
 'the','their','theirs','them','themselves','then','there','these','they','this','those','through','to','too','under','until','up','ve','very','was','wasn',"wasn't",'we','were','weren',"weren't",'what','when','where','which','while',
 'who','whom','why','will','with','won',"won't",'wouldn',"wouldn't",'y','you',"you'd","you'll","you're","you've", 'your','yours','yourself','yourselves'
 }

class WordcloudBuilder:

    def __init__(self, df: pd.DataFrame, width: int = 800, height: int = 400):
        self.df = df
        self.width = width
        self.height = height
        self.known_community_filler_words = set([
                'set',
                'via',
                'using',
                "learning",
                "toward",
                "towards",
            ])
        self.merge_tags = {
                '3d': '3D',
                '3D': '3D',
                'CLIP': 'CLIP',
                'clip': 'CLIP',
            }
        
        
    def create_wordcloud(self, col: str = 'relevant_tags'):
        all_tags = self.df[col].to_list()
        concat_tags = []
        for tags in all_tags:
            tags = eval(tags) if isinstance(tags, str) else []
            for t in tags:
                if t in self.merge_tags:
                    t = self.merge_tags[t]
                concat_tags.append(t)
        stop_words = set(stopwords)
        stop_words = stop_words.union(self.known_community_filler_words)
        tag_frequencies = Counter(concat_tags)
        wordcloud = WordCloud(width=self.width, 
                      height=self.height, 
                      background_color='white',
                      max_words=cfg.MAX_WORDCLOUD_WORDS,
                      colormap='viridis',
                      contour_color='steelblue',
                      random_state=400,
                     ).generate_from_frequencies(tag_frequencies)
        
        word_freq = wordcloud.words_
        words = list(word_freq.keys())
        freqs = list(word_freq.values())
        # Create a DataFrame
        word_data = pd.DataFrame({"word": words, "frequency": freqs})

        # Calculate ranks
        word_data["rank"] = word_data["frequency"].rank(method='min', ascending=False).astype(int)
        word_data["size"] = [wc[1] for wc in wordcloud.layout_]

        for i, layout_ in enumerate(wordcloud.layout_):
            (word, frequency), font_size, (y, x), orientation, color = layout_
            # Calculate the approximate width and height of the word
            width = len(word) * font_size * 0.5  # 0.6 is an approximate width-to-height ratio for most fonts
            height = font_size
            # Calculate the center
            y_tl = y + height / 2
            x_tl = x + width / 2
            # Adjust the y-coordinate to be from the bottom-left corner
            y_tl = self.height - y_tl
            word_data.loc[i, "x"] = x_tl
            word_data.loc[i, "y"] = y_tl
            word_data.loc[i, "color"] = color

        return wordcloud, concat_tags, word_data

    
def create_a_wordcloud(data: pd.DataFrame, col: str):
    wc = WordcloudBuilder(df=data, width=cfg.WORDCL_WIDTH, height=cfg.WORDCL_HEIGHT)
    wordcloud, tags, word_data = wc.create_wordcloud(col)
    return wordcloud, tags, word_data


def wordcloud_to_plotly(word_data):
    fig = px.scatter(
        word_data,
        x="x",
        y="y",
        text="word",
        size="size",
        hover_data={'rank': True, 'word': False}  # Add rank to hover, hide the word
    )
    
    font_size = word_data["size"].to_list()
    colors = word_data["color"].to_list()
    
    fig.update_traces(
        mode="text",
        textposition="middle center",
        textfont={"size": [f//1.5 for f in font_size], "color": colors},
        hovertemplate='<b>Word:</b> %{text}<br><b>Rank:</b> %{customdata[0]}<extra></extra>'  # Custom hover template
    )

    fig.update_layout(
        template=cfg.theme,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        xaxis_title="",
        yaxis_title="",
        width=cfg.WORDCL_WIDTH,
        height=cfg.WORDCL_HEIGHT,
        autosize=True,
        margin=dict(t=20, r=20, b=20, l=20),
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        plot_bgcolor="white",
        xaxis_zeroline=True,
        yaxis_zeroline=True,
        xaxis_zerolinewidth=2,
        yaxis_zerolinewidth=2,
        shapes=[
            dict(
                type="rect",
                x0=0,
                y0=1,
                x1=1,
                y1=1.02,
                fillcolor="black",
            )
        ]
    )
    return fig
