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

    def get(self, request, *args, **kwargs):
        subscription = Subscription.objects.create(
            status='pending',
            type='talk',
            user=request.user,
        )
        self.generate_transaction(subscription)
        return HttpResponseRedirect("/dashboard/")


class NotificationView(View):

    def transaction(self, transaction_code):
        url_transacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS, transaction_code, settings.PAGSEGURO[    "email"], settings.PAGSEGURO["token"])
        url_notificacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS_NOTIFICATIONS, transaction_code, settings.PAGSEGURO["email"], settings.PAGSEGURO["token"])

        response = requests.get(url_transacao)
        if not response.ok:
            response = requests.get(url_notificacao)
        if response.ok:
            dom = etree.fromstring(response.content)
            status_transacao = int(dom.xpath("//status")[0].text)
            referencia = int(dom.xpath("//reference")[0].text)
            return status_transacao, referencia
        return None, None
