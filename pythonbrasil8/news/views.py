# -*- coding: utf-8 -*-
from datetime import date
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.simple import direct_to_template

from pythonbrasil8.news.models import Post

class NewsView(ListView):
    template_name = 'news.html'
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(published_at__lte=date.today()).order_by('-published_at')

news_view = NewsView.as_view()

def post_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return direct_to_template(request, 'post.html', {'post': post})
