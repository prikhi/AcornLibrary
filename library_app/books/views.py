from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse

from books.models import Book
from books.models import BookForm
from books import utils

# Create your views here.
class CreateBookView(SuccessMessageMixin, CreateView):

    model = Book
    form = BookForm
    template_name = 'books/entry.html'
    success_message = "%(title)s was added successfully"
    
    def get_success_url(self):
        return reverse('books:entry')
        
    def get_context_data(self, **kwargs):
    
        context = super(CreateBookView, self).get_context_data(**kwargs)
        context['action'] = reverse('books:entry')
        context['create'] = True
        
        return context
        

class UpdateBookView(SuccessMessageMixin, UpdateView):
    
    model = Book
    template_name = 'books/entry.html'
    success_message = "%(title)s was updated successfully"
    
    def get_success_url(self):
        return reverse('books:entry')
    
    def get_context_data(self, **kwargs):
    
        context = super(UpdateBookView, self).get_context_data(**kwargs)
        context['action'] = reverse('books:update', kwargs={'pk': self.get_object().id})
        
        return context


def entry(request, book=None):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ''.join(['\"', form.cleaned_data['title'], '\"', ' was added successfully.']))
            form = BookForm()
    else:
        form = BookForm()
        if book:
            form = BookForm(instance = Book.objects.get(pk=book))
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
    
    
def subjects(request):
    subjects = Book.subjects.all().order_by('name')
    context = {'subjects': subjects}
    return render(request, 'books/subjects.html', context)
