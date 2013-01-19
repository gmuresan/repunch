from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index'),
    url(r'^retailers/', 'views.retailers', name='retailer_info'),
    url(r'^contact/', 'views.contact', name='contact_info'),
    (r'^', include('account.urls')),
    (r'^', include('retailer.urls')),
    (r'^', include('mobile.urls')),
    (r'^', include('utility.urls')),
    #(r'^accounts/', include('registration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sample/data/$', 'retailer.views.sample_data'),
)

urlpatterns += staticfiles_urlpatterns()