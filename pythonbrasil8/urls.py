# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView
from registration.forms import RegistrationForm

from pythonbrasil8.subscription.views import NotificationView

from core.views import Home, AboutView , ScheduleView, SponsorsInfoView, VenueView, CustomSponsorsView, SponsorsJobsView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^sponsors/info/$', SponsorsInfoView.as_view(), name='sponsors-info'),
    url(r'^previous-editions/$', TemplateView.as_view(template_name="previous_editions.html"), name='previous-editions'),
    url(r'^news/$', TemplateView.as_view(template_name="news.html"), name='news'),
    url(r'^badges/$', TemplateView.as_view(template_name="badges.html"), name='badges'),
    url(r'^register/$', TemplateView.as_view(template_name="register.html"), name='register'),
    url(r'^sponsors/$', CustomSponsorsView.as_view(), name='custom-sponsors'),
    url(r'^schedule/$', ScheduleView.as_view(), name='schedule'),
    url(r'^sponsors/jobs/$', SponsorsJobsView.as_view(), name='sponsors-jobs'),
    url(r'about/$', AboutView.as_view(), name='about'),
    url(r'^venue/$', VenueView.as_view(), name='venue'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^notification/$', NotificationView.as_view(), name='notification'),

    url(r'^dashboard/', include('pythonbrasil8.dashboard.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'extra_context': {'registration_form': RegistrationForm()}}, name='auth_login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
