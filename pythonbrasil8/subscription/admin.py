from django.contrib import admin

from pythonbrasil8.subscription import models


def name(subscription):
    return subscription.user.get_profile().name
name.short_description = u"Name"


def status(subscription):
    status = u"pending"
    statuses = set([t.status for t in subscription.transaction_set.all()])
    for st in statuses:
        if st == u"canceled":
            status = u"canceled"
        elif st == "pending":
            status = u"pending"
        elif st == "done":
            status = u"confirmed"
            break
    return status
status.short_description = u"Status"


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (name, status)

admin.site.register(models.Subscription, SubscriptionAdmin)
