# CVPR Papers Dashboard

## Overview

The CVPR Paper Analysis Dashboard is a web application designed to help users analyze and visualize research papers from the CVPR 2024 conference. The app provides an interactive word cloud, bar plots, and detailed lists of papers based on selected tags and organizations. This makes it easier to explore the trends and key topics in the CVPR 2024 dataset.

### Dataset

The dataset used in this app is a CSV file containing the following columns:

- `title`: Title of the paper
- `authors`: Authors of the paper
- `institutes`: Affiliated institutions/organizations
- `abstract`: Abstract of the paper
- `project_link`: Link to the project page
- `paper_link`: Link to the paper
- `relevant_tags`: Tags relevant to the paper extracted from abstract
- `novelty_rating`: Novelty rating of the paper based on GPT4-o
- `impact_rating`: Impact rating of the paper based on GPT4-o

### Key Features

- **Interactive Word Cloud**: Visualize the most frequent tags in the dataset.
- **Tag-Based Bar Plots**: View the top 25 organizations or tags by paper count.
- **Detailed Paper List**: Explore detailed lists of papers filtered by selected tags and organizations.

## How to Use This App

1. **Word Cloud Interaction**:
   - Click on any word in the word cloud to add it to the selected tags.
   - The selected tags are displayed below the word cloud.

2. **Tag Dropdown**:
   - Select or type tags in the dropdown to add them to the selected tags list.
   - The bar plot and paper list update based on the selected tags.

3. **Bar Plot Interaction**:
   - Click on any bar in the plot to select an organization.
   - The paper list updates to show papers from the selected organization and tags.

4. **Paper List**:
   - The list of papers updates dynamically based on the selected tags and organization.
   - Each paper entry includes the title, authors, abstract, and links to the project and paper.

## Installation Instructions

To run the CVPR Paper Analysis Dashboard locally, follow these steps:

### Prerequisites

- Python 3.7 or higher
- Pip package manager

### Clone the Repository

```bash
conda create --name cvpr24 python=3.9
conda activate cvpr24
pip install -r requirements.txt
```

### Run the app

```bash
python app.py 
```