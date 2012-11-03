# -*- coding: utf-8 -*-
from transmeta import TransMeta

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    published_at = models.DateField(verbose_name=_(u'Published at'))
    content = models.TextField(verbose_name=_(u'Content'), help_text=_('Use markdown language'))
    slug = models.SlugField(max_length=255, verbose_name=_(u'Slug'), blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=_(u'Author'))

    class Meta:
        translate = ('title', 'content')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
