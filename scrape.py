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
nltk.download('punkt')


def scrape_website_content(url):
    """
    Function to scrape website content. Returns a list of 2 word string.
    """
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def get_names(spans):
    """
    Function to get names from a string. Returns a list of names.
    """
    return[ span.text.strip() for span in spans if is_name(span.text) ]

def get_links_from_url(page_contents):
    if page_contents is None:
        return []
    # clearn the links if they are not none
    lnks = page_contents.find_all('a')
    lnks = [link for link in lnks if link.get('href') is not None]
    return [link.get('href') for link in lnks  if 'ie.edu' in link.get('href')]

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


# get all names
names = set([ span.text for span in two_word_spans if is_name(span.text) ])

links = get_links_from_url(body)
# get all names
limit = 100
while len(links) > 0 and limit > 0:
    limit -= 1
    try:
        link = links.pop(0)
        print(link, names)
        page = scrape_website_content(link)
        if page is None:
            continue
        # two word spans
        spans = [ span for span in page.find_all('span') if len(span.text.split()) == 2 ]
        new_names = get_names(spans)
        # add all new names
        [ names.add(name) for name in new_names]
        links_on_link = get_links_from_url(page)
        links.extend(links_on_link)
    except:
        pass

# get all emails
# re check all names if they are not ALL CAPS or \n or \r
clean_names = [ name for name in names if not re.match(r'^[A-Z\s]+$', name) and not re.match(r'^\n$', name) and not re.match(r'^\r$', name) ]

print(clean_names)
