from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages

from books.models import Book
from books.models import BookForm

from lxml import html
import requests

# Create your views here.


def entry(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ''.join(['\"', form.cleaned_data['title'], '\"', ' was added successfully.']))
            form = BookForm()
    else:
        form = BookForm()
    return render(request, 'books/entry.html', {
        'form': form,
    })

def lookup(request):
    results = {'success': False}
    if request.method == 'GET':
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
                       'authors': ["test author 1", "test, author 2"],
                       'dewey_decimal': ''.join(dewey_decimal)}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book, }
    return render(request, 'books/index.html', context)
