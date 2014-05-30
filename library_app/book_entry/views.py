from django.shortcuts import render
from django.http import HttpResponse

from book_entry.models import Book

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def detail(request, isbn):
    book = Book.objects.get(isbn=isbn)
    title = book.title
    return HttpResponse("Title: %s" % title)
