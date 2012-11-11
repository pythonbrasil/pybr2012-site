from django.contrib import admin

from pythonbrasil8.subscription import models


def name(subscription):
    return subscription.user.get_profile().name
name.short_description = u"Name"


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (name, "status",)
    list_filter = ("status",)

admin.site.register(models.Subscription, SubscriptionAdmin)
