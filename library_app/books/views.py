from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from haystack.query import SearchQuerySet

from books.models import Book
from books.models import BookForm
from books.models import Category
from books.models import TaggedSubject
from books import utils


# Create your views here.
class CreateBookView(SuccessMessageMixin, CreateView):

    model = Book
    form_class = BookForm
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
    form_class = BookForm
    template_name = 'books/entry.html'
    success_message = "%(title)s was updated successfully"
    
    def get_success_url(self):
        return reverse('books:entry')
    
    def get_context_data(self, **kwargs):
    
        context = super(UpdateBookView, self).get_context_data(**kwargs)
        context['action'] = reverse('books:update', kwargs={'pk': self.get_object().id})
        
        return context


def lookup(request):
    results = {'success': False}
    if request.method == 'GET':
        results = utils.get_book_info(request)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
        
    
def subjects(request, book_type):
    if book_type=='fiction':
        queryset = Book.objects.filter(dewey_decimal__startswith='813')
        subjects = Book.subjects.filter(book__in=queryset).order_by('name')
        print(queryset.count())
    elif book_type=='non-fiction':
        queryset = Book.objects.exclude(dewey_decimal__startswith='813')
        subjects = Book.subjects.filter(book__in=queryset).order_by('name')
    else:
        subjects = Book.subjects.all().order_by('name')
    context = {
        'book_type': book_type,
        'subjects': subjects
    }
    return render(request, 'books/subjects.html', context)


def subject_results(request, book_type, subject):
    results = Book.objects.filter(subjects__name__in=[subject])
    if book_type=='fiction':
        results = results.filter(dewey_decimal__startswith='813')
    elif book_type=='non-fiction':
        results = results.exclude(dewey_decimal__startswith='813')    
    
    paginator = Paginator(results, 15)
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
    
    context = {
        'page': page,
        'paginator': paginator,
    }
    
    return render_to_response('search/search.html', context, context_instance=RequestContext(request))

    
def latest(request):
    results = Book.objects.order_by('-added_on')
    paginator = Paginator(results, 15)
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
    
    context = {
        'page': page,
        'paginator': paginator,
    }
    
    return render_to_response('search/search.html', context, context_instance=RequestContext(request))
    

def dewey(request):
    return render_to_response("books/dewey.html",
                          {'nodes': Category.objects.all()},
                          context_instance=RequestContext(request))
                          

def dewey_results(request, ddc):
    results = Book.objects.filter(dewey_decimal__startswith=ddc)
    paginator = Paginator(results, 15)
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
    
    context = {
        'page': page,
        'paginator': paginator,
    }
    
    return render_to_response('search/search.html', context, context_instance=RequestContext(request))
