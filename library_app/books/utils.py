import requests
from lxml import html, etree, objectify
import urllib
import json
import re
import string

def tags_from_strings(tag_string):
    return [t.strip() for t in tag_string.split('%') if t.strip()]


def string_from_tags(tags):
    return '%'.join(t.name for t in tags)
    
def get_book_info(request):
    success=True
    # Google's title and author data is cleaner, and they sometimes have a description, so we try them first     
    isbn = request.GET['isbn']
    api_key = 'AIzaSyD8fIqUMR_jtZ9PxS9j9uqnuoD3RKx6fB8'
    url = ('https://www.googleapis.com/books/v1/volumes?q=isbn:%s&key=%s') % (isbn, api_key)
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    if data['totalItems'] != 0:
        title = data['items'][0]['volumeInfo'].get('title', None)
        description = data['items'][0]['volumeInfo'].get('description', None)
        if not description:
            if 'searchInfo' in data['items'][0]:
                description = data['items'][0]['searchInfo'].get('textSnippet', None)
        authors = []
        if 'authors' in data['items'][0]['volumeInfo']:
            for author in data['items'][0]['volumeInfo']['authors']:
                authors.append(author)
    else:
        title=''
        authors=[]
        description=''
        success = False
    
    # Next we try OCLC classify to get the dewey decimal and subjects, and also other information if google couldn't find it
    url = ('http://classify.oclc.org/classify2/Classify?isbn=%s') % (isbn)
    root = objectify.fromstring(urllib.request.urlopen(url).read())
    response_code = root.response.attrib['code']
    if response_code == '4':
        # Multiple listings were found. Oh joy. We need to figure out which one of the listings corresponds to the book we're looking for. We do this by getting the titles of hte listings and comparing them word by word to the google title. We assign a score to each one based on how many matching words there are, and pick the highest scoring one.
        oclc_titles = [ el.attrib['title'] for el in root.works.iterchildren() ]
        max_score = 0
        highest_scoring_index = 0
        if title:
            exclude = string.punctuation
            google_title = title.lower()
            google_title = ''.join(ch for ch in google_title if ch not in exclude)
            google_title_split = google_title.split()
            for index, oclc_title in enumerate(oclc_titles):
                score=0
                ot = oclc_title.lower()
                ot = ''.join(ch for ch in ot if ch not in exclude)
                oclc_title_split = ot.split()
                for x in google_title_split:
                    for y in oclc_title_split:
                        if x==y:
                            # square the length to more heavily weight longer matches
                            score = score+(len(x)**2)
                if score > max_score:
                    max_score=score
                    highest_scoring_index=index        
        
        #Hopefully we've found the best match, use the owi identifier to load the book information
        owi = root.works.work[highest_scoring_index].attrib['owi']
        url = ('http://classify.oclc.org/classify2/Classify?owi=%s') % (owi)
        root = objectify.fromstring(urllib.request.urlopen(url).read())
        response_code = root.response.attrib['code']
    if response_code == '0' or response_code == '2':
        # We successfully got the book information
        try:
            dewey_decimal = root.recommendations.ddc.mostPopular.attrib['nsfa']
        except:
            pass
        if dewey_decimal=='FIC':
            dewey_decimal = root.recommendations.ddc.mostPopular[1].attrib['nsfa']
        subjects = []
        try:
            subjects = [ el.text for el in root.recommendations.fast.headings.iterchildren()]
        except:
            pass
        if not authors:
            authors = []
            # do a whole bunch of bullshit to clean up the author data. Take out birth/death year, reverse "last, first" format
            for el in root.authors.iterchildren():
                text = el.text
                digit = re.search('\d', text)
                if digit:
                    text = text[:digit.start()-1]
                comma = text.find(',')
                if comma != -1:
                    text = ''.join([text[comma+2:], ' ', text[:comma]])
                comma = text.find(',')
                if comma != -1:
                    text = ''.join([text[:comma], '', text[comma+1:]])
                authors.append(text)
        if not title:
            title = root.work.attrib['title']
        if not description:
            description=''
        success = True
    else:
        success = False
    
    if success==True:
        results = {'success': True,
                   'title': title, 
                   'authors': authors,
                   'subjects': subjects,
                   'dewey_decimal': dewey_decimal,
                   'description': description}
    else:
        results = {'success': False}
    return results
