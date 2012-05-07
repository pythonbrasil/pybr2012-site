# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from pythonbrasil8.dashboard.views import IndexView, ProfileView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='dashboard-index'),
    url(r'^subscribe/$', 'pythonbrasil8.schedule.views.session_subscribe_view', name='session-subscribe'),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name="edit-profile")
)
