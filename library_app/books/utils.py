import requests
from lxml import html, etree

def tags_from_strings(tag_string):
    return [t.strip() for t in tag_string.split('%') if t.strip()]


def string_from_tags(tags):
    return '%'.join(t.name for t in tags)
    

def new_oclc_scrape(request):
    results = {'success': False}
    isbn = request.GET['isbn']
    page = etree.parse(''.join(['http://classify.oclc.org/classify2/Classify?isbn=', isbn, '&summary=true']))
    
    title = page.findtext('orderBy')
    if True:
        results = {'success': True,
                   'title': ''.join(title),  # Why are these lists?
                   'authors': 'Authors',
                   'dewey_decimal': '1.1'}
    return results  


def oclc_scrape(request):
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
