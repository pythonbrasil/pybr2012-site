from django.contrib import admin

from pythonbrasil8.schedule.models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type')
    list_filter = ('type',)


admin.site.register(Session, SessionAdmin)
