# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from pythonbrasil8.dashboard.views import IndexView, ProfileView
from pythonbrasil8.subscription.views import SubscriptionView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='dashboard-index'),
    url(r'^subscribe/$', 'pythonbrasil8.schedule.views.session_subscribe_view', name='session-subscribe'),
    url(r'^subscription/talk/$', SubscriptionView.as_view(), name='talk-subscription'),
    url(r'^profile/$', ProfileView.as_view(), name="edit-profile")
)
