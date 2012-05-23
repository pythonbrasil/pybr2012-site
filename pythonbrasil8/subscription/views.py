from django.views.generic import View
from django.http import HttpResponseRedirect
from django.conf import settings

from lxml import etree

from pythonbrasil8.subscription.models import Subscription, Transaction
from pythonbrasil8.dashboard.views import LoguinRequiredMixin

import requests


class SubscriptionView(LoguinRequiredMixin, View):

    def generate_transaction(self, subscription):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        payload["itemAmount1"] = "%.2f" % 255
        payload["reference"] = "%d" % subscription.pk
        response = requests.post(settings.PAGSEGURO_CHECKOUT, data=payload, headers=headers)

        if response.ok:
            dom = etree.fromstring(response.content)
            transaction_code = dom.xpath("//code")[0].text

            transaction = Transaction.objects.create(
                subscription=subscription,
                code=transaction_code,
            )
            return transaction
        return Transaction.objects.none()

    def post(self, request, *args, **kwargs):
        subscription = Subscription.objects.create(
            status='pending',
            type='talk',
            user=request.user,
        )
        self.generate_transaction(subscription)
        return HttpResponseRedirect("/dashboard/")
