from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lates.main.views.index', name='index'),
    url(r'^request$', 'lates.main.views.request_late', name='request'),
    url(r'^style.css$', 'lates.main.views.stylesheet', name='style.css'),
    url(r'^behavior.js$', 'lates.main.views.behavior', name='behavior.js'),
    url(r'json', 'lates.main.views.make_json', name='json'),
    url(r'([0-9]+)', 'lates.main.views.cancel', name='cancel'),
    # url(r'^lates/', include('lates.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
