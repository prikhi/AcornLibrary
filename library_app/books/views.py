from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages

from books.models import Book
from books.models import BookForm
from books import utils

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
        results = utils.get_book_info(request)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book, }
    return render(request, 'books/index.html', context)
