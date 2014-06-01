from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from book_entry.models import Book

from lxml import html
import requests

# Create your views here.
def lookup(request):
    return render(request, 'book_entry/lookup.html', {})

def entry(request):
    isbn = request.POST['isbn']

    page = requests.get(''.join(['http://classify.oclc.org/classify2/ClassifyDemo?search-standnum-txt=', isbn]))
    tree = html.fromstring(page.text)
    title = tree.xpath('//*[@id="display-Summary"]/dl/dd[1]/text()')
    author = tree.xpath('//*[@id="display-Summary"]/dl/dd[2]/a[1]/text()')
    ddc = tree.xpath('//*[@id="classSummaryData"]/tbody/tr[1]/td[2]/text()')

    context = {'isbn': isbn,
               'title': ''.join(title), #Why are these lists?
               'author': ''.join(author),
               'ddc': ''.join(ddc)
    }

    return render(request, 'book_entry/entry.html', context)

def save(request):
    b = Book(isbn = request.POST.get('isbn', 0),
             title = request.POST.get('title', ''),
             author = request.POST.get('author', ''),
             ddc = request.POST.get('ddc', ''))
    b.save()
    return redirect('/book_entry')

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book,}
    return render(request, 'book_entry/index.html', context)
