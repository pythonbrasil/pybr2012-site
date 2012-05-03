# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='dashboard-index'),
    url(r'^subscribe/$', 'pythonbrasil8.schedule.views.session_subscribe_view', name='session-subscribe'),
)
