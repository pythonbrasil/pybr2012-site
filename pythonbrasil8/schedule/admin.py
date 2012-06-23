from django.contrib import admin

from pythonbrasil8.schedule.models import Session, Track


class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type')
    list_filter = ('type',)

admin.site.register(Session, SessionAdmin)


class TrackAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Track, TrackAdmin)
