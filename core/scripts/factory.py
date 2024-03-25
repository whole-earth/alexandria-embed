# factory.py - Edward Rose
# This file computes the pipeline process of raw -> clean -> embedded for all of the artifacts listed and
#   adds them to the Django DB for JSON output.

# Pyhton Libs
import csv
import os
import string
# Django Libs
from django.utils import timezone
from core.models import Artifact
# 3rd Party Libs
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from openai import OpenAI


def run():

    # Pathing for manage.py
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_file_path = os.path.join(project_root, 'data', 'data.csv')

    # Preliminaries
    stop = stopwords.words('english')
    client = OpenAI()

    # TODO: Iterator should be 'open-ended' to allow iter on any properly formatted raw_data
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Clean Data
            clean_row = row
            
            ## Clean Title
            clean_row['title'] = clean_row['title'].str.lower()
            clean_row['title'] = remove_punctuation(clean_row['title'])

            ## Clean Description
            clean_row['description_cleaned'] = clean_row['description'].str.lower()
            clean_row['description_cleaned'] = remove_punctuation(clean_row['description_cleaned'])
            clean_row['description_cleaned'] = remove_stopwords(stop, clean_row['description_cleaned'])


            # Tokenize Data
            clean_row['description_tokenized'] = tokenize_desc(clean_row['description_cleaned'])


            # Embed Data

            # Dimensionality Reduction  
            # TODO

            # ? Graph/Figure of Dimensionally Reduced Embeddings ? for testing purposes only


            # Create the Artifact
            instance = Artifact(
                title=row['title'],
                description=row['description'],
                descriptionWC=row['description_wc']
            )

            # Save to DB
            #instance.save()

            print(instance.title)
            break

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

def get_embed(text, model='text-embedding-3-small', format='float', dimensions='1536'):
    # TODO
    embed_raw = ''
    return embed_raw

