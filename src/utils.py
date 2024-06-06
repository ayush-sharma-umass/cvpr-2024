import pandas as pd
import numpy as np
from collections import defaultdict

def create_tag_to_organizations_map(data: pd.DataFrame, valid_tags: list[str]):
    """
    Returns a dict such that
    { 
        tag1: 
            {
                'org1': ['title1', 'title2' ... ],
                'org2': ['title1', 'title2' ... ],
            },
        tag2:
            {
                'org1': ['title1', 'title2' ... ],
                'org3': ['title1', 'title2' ... ],
            },
        ...
    }
    """
    tag_to_orgs = {}
    for i, row in data.iterrows():
        tags = eval(row['relevant_tags'])
        orgs = eval(row['institutes']) if isinstance(row['institutes'], str) > 0 else []
        for tag in tags:
            if tag in valid_tags:
                if tag not in tag_to_orgs:
                    tag_to_orgs[tag] = {}
                for org in orgs:
                    if org not in tag_to_orgs[tag]:
                        tag_to_orgs[tag][org] = []
                    tag_to_orgs[tag][org].append(row['title'])
    return tag_to_orgs

def create_organization_to_tags_map(data: pd.DataFrame, valid_orgs: list[str]):
    """
    Returns a dict such that
    { 
        org1: 
            {
                'tag1': ['title1', 'title2' ... ],
                'tag2': ['title1', 'title2' ... ],
            },
        org1:
            {
                'tag1': ['title1', 'title2' ... ],
                'tag2': ['title1', 'title2' ... ],
            },
        ...
    }
    """
    org_to_tags = {}
    for i, row in data.iterrows():
        tags = eval(row['relevant_tags'])
        orgs = eval(row['institutes']) if isinstance(row['institutes'], str) > 0 else []
        for org in orgs:
            if org in valid_orgs:
                if org not in org_to_tags:
                    org_to_tags[org] = {}
                for tag in tags:
                    if tag not in org_to_tags[org]:
                        org_to_tags[org][tag] = []
                    org_to_tags[org][tag].append(row['title'])
    return org_to_tags

def count_papers_with_all_keys(keys_to_paper_map: dict, keys: list):
    """"
    :param keys_to_paper_map: dict
    key_to_paper_map is a dict such that
    { 
        tag1: 
            {
                'org1': ['title1', 'title2' ... ],
                'org2': ['title1', 'title2' ... ],
            },
        tag2:
            {
                'org1': ['title1', 'title2' ... ],
                'org3': ['title1', 'title2' ... ],
            },
        ...
    }
    OR
    { 
        org1: 
            {
                'tag1': ['title1', 'title2' ... ],
                'tag2': ['title1', 'title2' ... ],
            },
        org1:
            {
                'tag1': ['title1', 'title2' ... ],
                'tag2': ['title1', 'title2' ... ],
            },
        ...
    }
    :param keys: list
    keys can be alist of tags or a list of organizations
    :returns a dict such that
    { [all keys in the list]: 
        {
            'org1': 2,
            'org2': 3,
        },
    }

    OR

     { [all keys in the list]: 
        {
            'tag1': 2,
            'tag2': 3,
        },
    }
    """
    paper_counts = {}

    # Get the list of organizations for the first tag
    if keys:
        first_key = keys[0]
        subkeys_for_first_key = keys_to_paper_map.get(first_key, {})

        # Iterate over the organizations and their papers for the first tag
        for subkey, papers in subkeys_for_first_key.items():
            # Initialize a set of papers for intersection
            intersected_papers = set(papers)

            # Intersect with papers of the remkeying tags
            for key in keys[1:]:
                subkeys_for_first_key = keys_to_paper_map.get(key, {}).get(subkey, [])
                intersected_papers.intersection_update(subkeys_for_first_key)

            # Count the intersected papers
            paper_count = len(intersected_papers)
            if paper_count > 0:
                paper_counts[subkey] = paper_count
    return paper_counts

def create_list_of_papers_from_tags_and_orgs(data: pd.DataFrame, tags: list[str], orgs: list[str]):
    """
    Returns a list of papers that contain all the tags and organizations in the input lists
    :param data: pd.DataFrame
    :param tags: list
    :param orgs: list
    """
    papers = []
    for i, row in data.iterrows():
        tags_row = eval(row['relevant_tags'])
        orgs_row = eval(row['institutes']) if isinstance(row['institutes'], str) > 0 else []
        if set(tags).issubset(tags_row) and set(orgs).issubset(orgs_row):
            papers.append(row)
    return papers