from dataclasses import dataclass, field

cfg = {
    'page_title': "CVPR 2024",
    'DATA_DIR': "../data",
    'DATA_CSV': "large-cvpr-24-with-openai-response-and-institutes.csv",
    'RELEVANT_TAGS': 'relevant_tags',
    'RELEVANT_ORGS': 'institutes',
    'WORDCL_WIDTH': 800,
    'WORDCL_HEIGHT': 400,
    'BARPLOT_HT': 1000,
    'theme' :'seaborn',
    'MAX_WORDCLOUD_WORDS': 120,
}


@dataclass
class Config:
    page_title: str
    DATA_DIR: str
    DATA_CSV: str
    RELEVANT_TAGS: str
    RELEVANT_ORGS: str
    WORDCL_WIDTH: int
    WORDCL_HEIGHT: int
    BARPLOT_HT: int
    theme: str
    MAX_WORDCLOUD_WORDS: int = field(default=120)


def create_config() -> Config:
    return Config(**cfg)
