# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from mittun.registration.views import SubscribeView
from pythonbrasil8.subscription.views import NotificationView

from core.views import Home, SuccessfulPreRegistration, SponsorsInfoView, VenueView, CustomSponsorsView, SponsorsJobsView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^pre-registration/$', SubscribeView.as_view(), name='pre-registration'),
    url(r'^sponsors/info/$',  SponsorsInfoView.as_view(), name='sponsors-info'),
    url(r'^sponsors/$',  CustomSponsorsView.as_view(), name='custom-sponsors'),
    url(r'^schedule/$',  CustomSponsorsView.as_view(), name='schedule'),
    url(r'^sponsors/jobs/$', SponsorsJobsView.as_view(), name='sponsors-jobs'),
    url(r'^previous_version/$', TemplateView.as_view(template_name="previous_edition.html"), name='previous-version'),
    url(r'^successful-subscribed/$', SuccessfulPreRegistration.as_view(), name='pre-registration-success'),
    url(r'^venue/$',  VenueView.as_view(), name='venue'),
    url(r'^mittun/', include('mittun.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^notification/$', NotificationView.as_view(), name='notification'),

    url(r'^dashboard/', include('pythonbrasil8.dashboard.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^auth/', include('registration.auth_urls', namespace="auth", app_name="registration")),
    url(r'^admin/', include(admin.site.urls)),
)
