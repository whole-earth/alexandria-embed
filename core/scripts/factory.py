# factory.py - Edward Rose
# This file computes the pipeline process of raw -> clean -> embedded for all of the artifacts listed and
#   adds them to the Django DB for JSON output.

# Pyhton Libs
import csv
import os
import string
import pandas as pd
import umap
# Django Libs
from django.utils import timezone
from core.models import Artifact
# 3rd Party Libs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from openai import OpenAI


def run():

    # Pathing for manage.py
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_file_path = os.path.join(project_root, 'data', 'data.csv')
    new_csv_file = os.path.join(project_root, 'data', 'data2.csv')
    embed_raw_file = os.path.join(project_root, 'data', 'embed_raw.txt')
    # Preliminaries
    stop = stopwords.words('english')
    client = OpenAI()

    dtype_mapping = {
        'round': int,
        'title': str,
        'description': str,
        'description_wc': int,
        'thumbnail': str,
        'redirect': str,
        'Year': int
    }

    default_values = {
        'round': 0,
        'title': 'N/A',
        'description': 'N/A',
        'description_wc': 0,
        'thumbnail': './thumbnail.png',
        'redirect': 'N/A',
        'Year': 0
    }

    df = pd.read_csv(csv_file_path)
    df['round'] = df['round'].fillna(0)
    df['title'] = df['title'].fillna('')
    df['description'] = df['description'].fillna('')
    df['description_wc'] = df['description_wc'].fillna(0)
    df['thumbnail'] = df['thumbnail'].fillna('./thumbnail.png')
    df['redirect'] = df['redirect'].fillna('')
    df['Year'] = df['Year'].fillna(0)

    df = df.astype(dtype_mapping)

    df_cleaned = df.copy()

    embed_raw_arr = []

    # TODO: Iterator should be 'open-ended' to allow iter on any properly formatted raw_data
    for index, clean_row in df_cleaned.iterrows():
        # Clean Data

        ## Clean Description
        description_cleaned = clean_row['description']
        description_cleaned = description_cleaned.lower()
        description_cleaned = remove_punctuation(description_cleaned)
        description_cleaned = remove_stopwords(stop, description_cleaned)
        # clean_row['description_cleaned'] = clean_row['description'].lower()
        # clean_row['description_cleaned'] = remove_punctuation(clean_row['description_cleaned'])
        # clean_row['description_cleaned'] = remove_stopwords(stop, clean_row['description_cleaned'])

        # Tokenize Data
        description_tokenized = tokenize_desc(description_cleaned)
        # clean_row['description_tokenized'] = tokenize_desc(clean_row['description_cleaned'])

        # Embed Data
        embed_raw = get_embed(description_tokenized, client)
        embed_raw_arr.append(embed_raw)
        embed_raw_str = ','.join([str(x) for x in embed_raw])
        append_to_file(index, embed_raw_str, embed_raw_file)

        # # Dimensionality Reduction  
        # # TODO
        embed_3d = 1
        # embed_3d = 1
        # umap_reducer = umap.UMAP(n_components=3)
        # embed_3d = umap_reducer.fit_transform(embed_raw)


        # ? Graph/Figure of Dimensionally Reduced Embeddings ? for testing purposes only


        # Create the Artifact
        # instance = Artifact(
        #     title=row['title'],
        #     description=row['description'],
        #     descriptionWC=clean_row['description_wc']
        # )

        # Save to CSV
        df_cleaned.at[index, 'description_cleaned'] = description_cleaned
        df_cleaned.at[index, 'description_tokenized'] = ','.join([str(x) for x in description_tokenized])
        df_cleaned.at[index, 'embed_raw'] = embed_raw_str
        df_cleaned.at[index, 'embed_3d'] = embed_3d

    umap_reducer = umap.UMAP(n_components=3)
    embed_3d_pts = umap_reducer.fit_transform(embed_raw_arr)

    df_cleaned['embed_3d'] = [','.join(map(str, row)) for row in embed_3d_pts]

    df_cleaned.to_csv(new_csv_file, index=False)
    print(df_cleaned.head())
    return 

def remove_punctuation(text):
    for char in string.punctuation:
        text = text.replace(char, '')
    return text

def remove_stopwords(stop, text):
    return ' '.join([word for word in text.split() if word not in stop])

def tokenize_desc(text):
    # TODO: Should it be just words? Why are we cleaning, then? 
    sentence_tokens = sent_tokenize(text)
    word_tokens = word_tokenize(text)
    return word_tokens

def get_embed(text, client, model='text-embedding-3-small', format='float', dimensions=1536):
    # TODO
    input_text = " ".join(text)
    embed_raw = client.embeddings.create(input=input_text, model=model, dimensions=dimensions)
    return embed_raw.data[0].embedding

def append_to_file(index, value, file_path):
    with open(file_path, 'a') as file:
        file.write(str(index) + " " + str(value) + '\n')
