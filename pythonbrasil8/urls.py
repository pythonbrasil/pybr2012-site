# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from mittun.registration.views import SubscribeView

from core.views import Home, SuccessfulPreRegistration, VenueView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^pre-registration/$', SubscribeView.as_view(), name='pre-registration'),
    url(r'^successful-subscribed/$', SuccessfulPreRegistration.as_view(), name='pre-registration'),
	url(r'^venue/$',  VenueView.as_view(), name='venue'),
    url(r'^mittun/', include('mittun.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)
