from django.conf.urls.defaults import patterns, url
from core.views import Home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$',  Home.as_view(), name='Home'),
    # url(r'^pythonbrasil8/', include('pythonbrasil8.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
