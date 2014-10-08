import requests
from lxml import html, etree, objectify
import urllib
import json
import re

def tags_from_strings(tag_string):
    return [t.strip() for t in tag_string.split('%') if t.strip()]


def string_from_tags(tags):
    return '%'.join(t.name for t in tags)
    
def get_book_info(request):
    success=True       
    isbn = request.GET['isbn']
    api_key = 'AIzaSyD8fIqUMR_jtZ9PxS9j9uqnuoD3RKx6fB8'
    url = ('https://www.googleapis.com/books/v1/volumes?q=isbn:%s&key=%s') % (isbn, api_key)
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    if data['totalItems'] != 0:
        title = data['items'][0]['volumeInfo']['title']
        #description = data['items'][0]['volumeInfo']['description']
        description = data['items'][0]['volumeInfo'].get('description', None)
        if not description:
            if 'searchInfo' in data['items'][0]:
                description = data['items'][0]['searchInfo'].get('textSnippet', None)
        authors = []
        if 'authors' in data['items'][0]['volumeInfo']:
            for author in data['items'][0]['volumeInfo']['authors']:
                authors.append(author)
    else:
        success = False
    
    url = ('http://classify.oclc.org/classify2/Classify?isbn=%s') % (isbn)
    root = objectify.fromstring(urllib.request.urlopen(url).read())
    if root.response.attrib['code'] != '101':
        dewey_decimal = root.recommendations.ddc.mostPopular.attrib['nsfa']
        subjects = [ el.text for el in root.recommendations.fast.headings.iterchildren()]
        if not authors:
            for el in root.authors.iterchildren():
                text = el.text
                digit = re.search('\d', text)
                if digit:
                    text = text[:digit.start()-1]
                comma = text.find(',')
                if comma != -1:
                    text = ''.join([text[comma+2:], ' ', text[:comma]])
                authors.append(text)
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

def oclc_scrape(request):
    results = {'success': False}
    isbn = request.GET['isbn']
    url = ''.join(['http://classify.oclc.org/classify2/Classify?isbn=', isbn, '&summary=true'])

    root = objectify.fromstring(urllib.request.urlopen(url).read())
    title = root.work.attrib['title']
    authors = []
    for author in root.authors.author:
        authors.append(author.text)   
    dewey_decimal = root.recommendations.ddc.mostPopular.attrib['nsfa']
    
    if True:
        results = {'success': True,
                   'title': title, 
                   'authors': authors,
                   'dewey_decimal': dewey_decimal}
    return results  


def old_oclc_scrape(request):
    results = {'success': False}
    isbn = request.GET['isbn']
    page = requests.get(''.join(['http://classify.oclc.org/classify2/ClassifyDemo?search-standnum-txt=', isbn]))
    tree = html.fromstring(page.text)
    if not tree.xpath('//*[@id="display-Summary"]/dl/dd[1]/text()'):  # Oh dear god, please fix me
        page = requests.get(''.join(['http://classify.oclc.org', ''.join(tree.xpath('//*[@id="results-table"]/tbody/tr[1]/td[1]/span[1]/a/@href'))]))
        tree = html.fromstring(page.text)
    title = tree.xpath('//*[@id="display-Summary"]/dl/dd[1]/text()')
    authors = tree.xpath('//*[@id="display-Summary"]/dl/dd[2]/a[1]/text()')
    dewey_decimal = tree.xpath('//*[@id="classSummaryData"]/tbody/tr[1]/td[2]/text()')
    if title:
        results = {'success': True,
                   'title': ''.join(title),  # Why are these lists?
                   'authors': authors,
                   'dewey_decimal': ''.join(dewey_decimal)}
    return results
