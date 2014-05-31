from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from book_entry.models import Book

from lxml import html
import requests

# Create your views here.
def lookup(request):
    context = {'book': 1}
    return render(request, 'book_entry/lookup.html', context)

def do_lookup(request):
    isbn = request.POST['isbn']

    page = requests.get(''.join(['http://classify.oclc.org/classify2/ClassifyDemo?search-standnum-txt=', isbn]))
    tree = html.fromstring(page.text)
    title = tree.xpath('//*[@id="display-Summary"]/dl/dd[1]/text()')
    author = tree.xpath('//*[@id="display-Summary"]/dl/dd[2]/a[1]/text()')
    ddc = tree.xpath('//*[@id="classSummaryData"]/tbody/tr[1]/td[2]/text()')
    return HttpResponse(ddc)

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book,}
    return render(request, 'book_entry/index.html', context)
