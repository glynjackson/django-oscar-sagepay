from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


from django.conf.urls import patterns, include, url
from oscar.app import application

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)), #admin site
    (r'^pages/', include('django.contrib.flatpages.urls')),
    (r'', include(application.urls)),
)
