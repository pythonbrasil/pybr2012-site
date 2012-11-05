# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from pythonbrasil8.news.feed import NewsFeed

urlpatterns = patterns('pythonbrasil8.news.views',
    url(r'^$', 'news_view', name='main'),
    url(r'^feed/$', NewsFeed(), name='feed'),
    url(r'^(?P<post_slug>[\w\d-]+)/$', 'post_view', name='post'),
)
