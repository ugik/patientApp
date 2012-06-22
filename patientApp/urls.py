from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'entry.views.HomePage'),
    (r'^register/$', 'entry.views.PatientRegistration'),
    (r'^login/$', 'entry.views.LoginRequest'),
    (r'^logout/$', 'entry.views.LogoutRequest'),
    (r'^profile/$', 'entry.views.Profile'),
    (r'^entry/$', 'entry.views.AddEntry'),
    (r'^hello/$', 'entry.views.hello'),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]*)-(?P<token>.*)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^code/$', direct_to_template, {'template': 'code.html', 'extra_context': {'showDirect': True}}),

    url(r'^admin/', include(admin.site.urls)),
)

