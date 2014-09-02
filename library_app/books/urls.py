from django.conf.urls import patterns, url, include
from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm

from books import views

urlpatterns = patterns('',
    url(r'^$', views.lookup, name='lookup'),
    #url(r'^do_lookup$', views.do_lookup, name='do_lookup'),
    url(r'^entry$', views.entry, name='entry'),
    url(r'^entry/(\d+)$', views.entry, name='edit'),
    url(r'^lookup/$', views.lookup, name='lookup'),
    url(r'^(?P<isbn>\d+)/$', views.detail, name='detail'),
    url(r'^search/', search_view_factory(
        view_class=SearchView,
        form_class=SearchForm
    ), name='haystack_search')
)
