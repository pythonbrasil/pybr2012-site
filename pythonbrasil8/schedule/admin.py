# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pythonbrasil8.schedule.models import Session, Track, ProposalVote


def coalesce(*args):
    for arg in args:
        if arg:
            return arg


class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "speaker_names", "track", "status",)
    list_filter = ("type", "status",)

    def speaker_names(self, obj):
        speakers = [coalesce(s.accountprofile.name, s.username) for s in obj.speakers.all().order_by("username")]
        return ", ".join(speakers)

    speaker_names.short_description = _("Speakers")

admin.site.register(Session, SessionAdmin)

class TrackAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ProposalVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "vote")

admin.site.register(Track, TrackAdmin)
admin.site.register(ProposalVote, ProposalVoteAdmin)
