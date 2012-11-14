# -*- coding: utf-8 -*-
from django.contrib import admin

from pythonbrasil8.dashboard import models


class AccountProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name"]
    list_filter = ["type"]

admin.site.register(models.AccountProfile, AccountProfileAdmin)
