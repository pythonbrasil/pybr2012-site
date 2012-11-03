# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from pythonbrasil8.news.models import Post

class NewsView(TemplateView):
    template_name = 'news.html'

    def get_context_data(self, *args, **kwargs):
        context = super(NewsView, self).get_context_data(*args, **kwargs)
        context['posts'] = Post.objects.all().order_by('-published_at')

        return context

news_view = NewsView.as_view()
