from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from book_entry.models import Book

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def detail(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    context = {'book': book,}
    return render(request, 'book_entry/index.html', context)
