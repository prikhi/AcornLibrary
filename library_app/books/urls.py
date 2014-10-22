from django.conf.urls import patterns, url, include
from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm
from django.views.generic import TemplateView, UpdateView

from books import views
from books.models import Book, BookForm

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="books/index.html")),
    url(r'^entry$', views.CreateBookView.as_view(), name='entry'),
    url(r'^entry/(?P<pk>\d+)$', views.UpdateBookView.as_view(), name='update'),
    url(r'^lookup/$', views.lookup, name='lookup'),
    url(r'^subjects$', views.subjects, name='subjects'),
    url(r'^subjects/(?P<subject>.+)$', views.subject_results, name='subject_results'),
    #url(r'^(?P<isbn>\d+)/$', views.detail, name='detail'),
    url(r'^search/', search_view_factory(
        view_class=SearchView,
        form_class=SearchForm
    ), name='haystack_search'),
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^dewey$', views.dewey, name='dewey'),
    url(r'^dewey/(?P<ddc>\d+)$', views.dewey_results, name='dewey_results'),
)
