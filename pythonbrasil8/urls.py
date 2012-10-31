# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.views.generic import TemplateView
from registration.forms import RegistrationForm

from pythonbrasil8.subscription.views import NotificationView

from core.views import (Home, AboutView, SponsorsInfoView, VenueView,
                        CustomSponsorsView, SponsorsJobsView)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^sponsors/info/$', SponsorsInfoView.as_view(), name='sponsors-info'),
    url(r'^previous-editions/$', TemplateView.as_view(template_name="previous_editions.html"), name='previous-editions'),
    url(r'^news/$', TemplateView.as_view(template_name="news.html"), name='news'),
    url(r'^badges/$', TemplateView.as_view(template_name="badges.html"), name='badges'),
    url(r'^register/$', TemplateView.as_view(template_name="register.html"), name='register'),
    url(r'^sponsors/$', CustomSponsorsView.as_view(), name='custom-sponsors'),
    url(r'^sponsors/jobs/$', SponsorsJobsView.as_view(), name='sponsors-jobs'),

    url(r'^schedule/$', 'pythonbrasil8.schedule.views.schedule', name='schedule'),
    url(r'^schedule/vote/?$', 'pythonbrasil8.schedule.views.vote_page',
        name='vote_page'),
    url(r'^schedule/vote/(?P<proposal_id>[0-9]+)/(?P<type_of_vote>\w+)?$',
        'pythonbrasil8.schedule.views.proposal_vote',
        name='proposal_vote'),
    url(r'^schedule/(?P<track_slug>[^/]+)/?$',
        'pythonbrasil8.schedule.views.track_page', name='track-page'),
    url(r'^schedule/(?P<track_slug>[^/]+)/(?P<proposal_slug>.*)/?$',
        'pythonbrasil8.schedule.views.proposal_page', name='proposal-page'),

    url(r'about/$', AboutView.as_view(), name='about'),
    url(r'^venue/$', VenueView.as_view(), name='venue'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^notification/$', NotificationView.as_view(), name='notification'),

    url(r'^dashboard/', include('pythonbrasil8.dashboard.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'extra_context': {'registration_form': RegistrationForm()}}, name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name='auth_logout'),
    url(r'^accounts/password/reset/$', password_reset, {'email_template_name': 'email_password_reset.txt', 'subject_template_name': 'email_password_reset_title.txt', 'template_name': 'password_reset.html'}, name='password_reset'),
    url(r'^accounts/password/reset/done/$', TemplateView.as_view(template_name="password_reset_sent.html"), name='password_reset_sent'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {"template_name": "password_reset_confirm.html"}, name='password_reset_confirm'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
