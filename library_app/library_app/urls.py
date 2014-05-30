from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'library_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^book_entry/', include('book_entry.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
