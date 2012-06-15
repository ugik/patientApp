from django.conf.urls import patterns, include, url
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
    url(r'^admin/', include(admin.site.urls)),
)

