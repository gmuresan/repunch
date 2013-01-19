from django.conf.urls.defaults import patterns, include, url
from django.contrib import auth

urlpatterns = patterns('',
    url(r'^register/$', 'account.views.register'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/retailer/login.html'}, name='login'),
    url(r'^logout/$', 'account.views.logoutUser'),
    url(r'^vault/$', 'account.views.vault'),
    url(r'^retailer/register/$', 'account.views.register_retailer', name='register_retailer'),
    url(r'^retailer/code/$', 'account.views.registration_code'),
    url(r'^settings/$', 'account.views.edit_account', name='edit_account'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change', name='change_password'),
    url(r'^change_password_done/$', 'django.contrib.auth.views.password_change_done', name='change_password_done'),
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset' , name='reset_password'),
    url(r'^reset_password_done/$', 'django.contrib.auth.views.password_reset_done', name='reset_password_done'),
    url(r'^reset_password_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='reset_password_confirm'),
    url(r'^reset_password_complete/$', 'django.contrib.auth.views.password_reset_complete', name='reset_password_complete'),

)
