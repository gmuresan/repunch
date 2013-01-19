from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^fb/at', 'utility.facebook_functions.fb_get_access_token', name='fb_get_access_token'),

)
