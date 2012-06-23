# -*- coding: utf-8 -*-
import transmeta

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Track(models.Model):
    __metaclass__ = transmeta.TransMeta

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.CharField(max_length=2000, verbose_name=_("Description"))

    class Meta:
        translate = ("name", "description")

    def __unicode__(self):
        return self.name

SESSION_TYPES = (
    ("tutorial", "tutorial",),
    ("talk", "talk"),
)

LANGUAGE_CHOICES = (
    ("pt", _("Portuguese")),
    ("en", _("English")),
    ("es", _("Spanish")),
)


class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=SESSION_TYPES)
    tags = models.CharField(max_length=255)
    speakers = models.ManyToManyField(auth_models.User)
    track = models.ForeignKey(Track)
    language = models.CharField(max_length=2, verbose_name=_("Language"), choices=LANGUAGE_CHOICES)
