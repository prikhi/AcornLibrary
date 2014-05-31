from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from book_entry.models import Book

# Create your views here.
def lookup(request):
    context = {'book': 1}
    return render(request, 'book_entry/lookup.html', context)

def do_lookup(request):
    isbn = request.POST['isbn']
    
    return HttpResponse(isbn)

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book,}
    return render(request, 'book_entry/index.html', context)
