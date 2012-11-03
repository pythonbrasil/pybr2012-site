# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from pythonbrasil8.news.models import Post

urlpatterns = patterns('pythonbrasil8.news.views',
    url(r'^$', 'news_view', name='main'),
    #url(r'^posts/(?P<post_slug>[\w\d-]+)/$', ProductView.as_view(), name='post'),
)
