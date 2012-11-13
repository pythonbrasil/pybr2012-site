# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from lxml import etree

PRICES = {
    'Student': 150,
    'APyB Associated': 150,
    'Speaker': 150,
    'Individual': 250,
    'Corporate': 350
}


class Subscription(models.Model):

    TYPE = (
        ('tutorial', 'tutorial',),
        ('talk', 'talk'),
    )

    STATUSES = (
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
        ('sponsor', 'Sponsor'),
    )

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=25, choices=TYPE)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')

    def done(self):
        return self.status == 'confirmed' or self.status == 'sponsor'


class Transaction(models.Model):
    subscription = models.ForeignKey('Subscription')
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_checkout_url(self):
        return settings.PAGSEGURO_WEBCHECKOUT + self.code

    @staticmethod
    def generate(subscription):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        profile = subscription.user.get_profile()
        price = PRICES[profile.type]
        payload["itemAmount1"] = "%.2f" % price
        payload['itemDescription1'] = ugettext(u'Payment of a %s Ticket in PythonBrasil[8] conference, 2012 edition') % ugettext(profile.type)
        payload["reference"] = "%d" % subscription.pk
        response = requests.post(settings.PAGSEGURO_CHECKOUT, data=payload, headers=headers)

        if response.ok:
            dom = etree.fromstring(response.content)
            transaction_code = dom.xpath("//code")[0].text

            transaction = Transaction.objects.create(
                subscription=subscription,
                code=transaction_code,
                status='pending',
                price=price
            )
            return transaction
        return Transaction.objects.none()
