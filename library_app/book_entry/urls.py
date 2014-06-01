from django.conf.urls import patterns, url

from book_entry import views

urlpatterns = patterns('',
    url(r'^$', views.lookup, name='lookup'),
    #url(r'^do_lookup$', views.do_lookup, name='do_lookup'),
    url(r'^entry$', views.entry, name='entry'),
    url(r'^save$', views.save, name='save'),
    url(r'^(?P<isbn>\d+)/$', views.detail, name='detail')
)
