# https://www.ie.edu/
# scrape the website for any names
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

url = 'https://www.ie.edu/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# get all two word span
body = soup.find('body')
spans = body.find_all('span')
two_word_spans = [ span for span in spans if len(span.text.split()) == 2 ]


nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def scrape_website_content(url):
    """
    Function to scrape website content. Returns a list of 2 word string.
    """
    pass

def get_names(string):
    """
    Function to get names from a string. Returns a list of names.
    """
    pass

def get_links_from_url(url):
    """
    Function to get all links from a url. Returns a list of links.
    """
    pass

def is_name(string):
    # Tokenize and POS tag the text
    tokens = word_tokenize(string)
    tags = pos_tag(tokens)

    # Chunk named entities
    tree = ne_chunk(tags)
    exclusion = ['department', "degree", 'campus', 'legal']
    if any(x in string.lower() for x in exclusion):
        return False

    # Check if any named entity is labeled as PERSON
    return any(chunk.label() == 'PERSON' for chunk in tree if hasattr(chunk, 'label'))

string = "Your string here"
print(is_name(string))


# get all names
names = [ span.text for span in two_word_spans if is_name(span.text) ]

# TODO Here define a crawler
# goes through all the links and get all the names


# get all emails
print(names)
