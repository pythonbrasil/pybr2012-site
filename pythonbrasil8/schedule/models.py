# -*- coding: utf-8 -*-

import transmeta
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


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
    (u"accepted", u"Accepted"),
    (u"confirmed", u"Confirmed"),
    (u"canceled", u"Canceled"),
)

SESSION_LEVELS = (
    (u"beginner", _(u"Beginner")),
    (u"intermediate", _(u"Intermediate")),
    (u"advanced", _(u"Advanced")),
)


class Track(models.Model):
    __metaclass__ = transmeta.TransMeta

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = models.SlugField(max_length=255, default=None, null=True,
            blank=True)
    description = models.CharField(max_length=2000,
            verbose_name=_("Description"))

    class Meta:
        translate = ("name", "description")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Track, self).save(*args, **kwargs)


class Session(models.Model):
    type = models.CharField(max_length=20, choices=SESSION_TYPES,
            verbose_name=_("Type"))
    track = models.ForeignKey(Track, verbose_name=_("Track"))
    audience_level = models.CharField(max_length=12, choices=SESSION_LEVELS,
            verbose_name=_("Audience level"))
    language = models.CharField(max_length=2, verbose_name=_("Language"),
            choices=LANGUAGE_CHOICES)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=255, default=None, null=True,
            blank=True)
    description = models.TextField(verbose_name=_("Description"))
    speakers = models.ManyToManyField(auth_models.User,
            verbose_name=_("Speakers"))
    status = models.CharField(max_length=10, choices=SESSION_STATUSES,
            default="proposed")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Session, self).save(*args, **kwargs)


class ProposalVote(models.Model):
    user = models.ForeignKey(auth_models.User)
    session = models.ForeignKey(Session)
    vote = models.IntegerField(default=0)
