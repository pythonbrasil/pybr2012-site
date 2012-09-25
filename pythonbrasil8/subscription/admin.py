from django.contrib import admin

from pythonbrasil8.subscription import models


class StatusFilter(admin.SimpleListFilter):
    title = u"Status"
    parameter_name = u"status"

    def lookups(self, *args, **kwargs):
        return (
            (u"pending", u"Pending"),
            (u"confirmed", u"Confirmed"),
            (u"canceled", u"Canceled"),
        )

    def queryset(self, request, queryset):
        v = self.value()
        return filter(lambda sub: status(sub) == v, queryset)


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
    list_display = (name, status,)
    list_filter = (StatusFilter,)

admin.site.register(models.Subscription, SubscriptionAdmin)
