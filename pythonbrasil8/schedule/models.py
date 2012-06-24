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
    ("talk", _("Talk")),
    ("tutorial", _("Tutorial"),),
)

LANGUAGE_CHOICES = (
    ("pt", _("Portuguese")),
    ("en", _("English")),
    ("es", _("Spanish")),
)

SESSION_STATUSES = (
    (u"proposed", u"Proposed"),
    (u"accepcted", u"Accepted"),
    (u"confirmed", u"Confirmed"),
    (u"canceled", u"Canceled"),
)


class Session(models.Model):
    type = models.CharField(max_length=20, choices=SESSION_TYPES, verbose_name=_("Type"))
    track = models.ForeignKey(Track, verbose_name=_("Track"))
    language = models.CharField(max_length=2, verbose_name=_("Language"), choices=LANGUAGE_CHOICES)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    speakers = models.ManyToManyField(auth_models.User, verbose_name=_("Speakers"))
    status = models.CharField(max_length=10, choices=SESSION_STATUSES, default="proposed")
