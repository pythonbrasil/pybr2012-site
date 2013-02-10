# -*- coding: utf-8 -*-
from datetime import date

from django.core.urlresolvers import reverse
from django.contrib.markup.templatetags.markup import markdown
from django.contrib.syndication.views import Feed

from pythonbrasil8.news.models import Post


class NewsFeed(Feed):
    title = 'PythonBrasil[8] News'
    description = 'News from PythonBrasil[8]'
    link = '/news/feed/'

    def items(self):
        qs = Post.objects.filter(published_at__lte=date.today())
        return qs.order_by('-published_at')

    def item_description(self, item):
        return markdown(item.content)

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('news:post', kwargs={'post_slug': item.slug})
