# https://www.ie.edu/
# scrape the website for any names
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.ie.edu/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# get all two word span
body = soup.find('body')
spans = body.find_all('span')
two_word_spans = [ span for span in spans if len(span.text.split()) == 2 ]



def scrape_website_content(url):
    """
    Function to scrape website content. Returns a list of 2 word string.
    """
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def get_names(spans):
    """
    Function to get names from a string. Returns a list of names.
    """
    return[ span.text.strip() for span in spans if is_name(span.text.strip()) ]

def get_links_from_url(page_contents):
    if page_contents is None:
        return []
    # clearn the links if they are not none
    lnks = page_contents.find_all('a')
    lnks = [link for link in lnks if link.get('href') is not None]
    return [link.get('href') for link in lnks  if 'ie.edu' in link.get('href')]


# Create a NER pipeline with the pre-trained model

# mdarhri00/named-entity-recognition
from transformers import pipeline

pipe = pipeline("token-classification", model="mdarhri00/named-entity-recognition")

from functools import cache

@cache
def is_name(string):

    # run the model
    result = pipe(string)
    r=[a['word'] for a in result if a['entity'] == "Person_Name"]
    bl = len(r) > 0
    return bl

# get all names
names = set([ span.text for span in two_word_spans if is_name(span.text) ])


links = get_links_from_url(body)
seen = set(links)
# get all names
limit = 1000
while len(links) > 0 and limit > 0:
    limit -= 1
    try:
        link = links.pop(0)
        page = scrape_website_content(link)
        if page is None:
            continue
        # two word spans
        # get all spans with more than one word
        spans = [span for span in page.find_all('span') if len(span.text.split()) < 5]
        print(len(spans))

        new_names = get_names(spans)
        print(link, len(links), len(names), len(new_names))
        # add all new names
        [ names.add(name) for name in new_names]
        links_on_link = [a for a in get_links_from_url(page) if a not in seen]
        for a in links_on_link:
            seen.add(a)
        links.extend(links_on_link)
        # save the names to a file
        df = pd.DataFrame(names, columns=['name'])
        df.to_csv('names.csv')
    except:
        pass

# get all emails
# re check all names if they are not ALL CAPS or \n or \r
clean_names = [ name for name in names if not re.match(r'^[A-Z\s]+$', name) and not re.match(r'^\n$', name) and not re.match(r'^\r$', name) ]

print(clean_names)
