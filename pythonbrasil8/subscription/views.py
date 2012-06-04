# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lxml import etree

from pythonbrasil8.core import mail
from pythonbrasil8.core.views import LoginRequiredMixin
from pythonbrasil8.dashboard.models import AccountProfile
from pythonbrasil8.subscription.models import PRICES, Subscription, Transaction


class SubscriptionView(LoginRequiredMixin, View):

    def generate_transaction(self, subscription):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        profile = AccountProfile.objects.get(user=subscription.user)
        price =  PRICES[profile.type]
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

    def get(self, request, *args, **kwargs):
        profile = AccountProfile.objects.filter(user=request.user)
        if not profile or not profile[0].name:
            msg = ugettext("In order to issue your registration to the conference, you need to complete your profile.")
            messages.error(request, msg, fail_silently=True)
            url = "%s?next=%s" % (reverse("edit-profile"), request.path)
            return HttpResponseRedirect(url)
        subscription = Subscription.objects.create(
            type='talk',
            user=request.user,
        )
        t = self.generate_transaction(subscription)

        if not t:
            self._notify_staff(request.user)
            subscription.delete()
            url = "/dashboard/"
            messages.error(request, ugettext("Failed to generate a transaction within the payment gateway. Please contact the event staff to complete your registration."), fail_silently=True)
        else:
            url = settings.PAGSEGURO_WEBCHECKOUT + t.code
        return HttpResponseRedirect(url)

    def _notify_staff(self, user):
        msg = u"There was a failure in the communication with PagSeguro, the user %(email)s could not be registered."
        kw = {"email": user.email}
        body = msg % kw
        mail.send(settings.EMAIL_HOST_USER, ["organizers@python.org.br"], "PagSeguro Communication Failure", body)


class NotificationView(View):

    def __init__(self, *args, **kwargs):
        self.methods_by_status = {
            3: self.transaction_done,
            7: self.transaction_canceled,
        }
        return super(NotificationView, self).__init__(*args, **kwargs)

    def transaction(self, transaction_code):
        url_transacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS,
                                                     transaction_code,
                                                     settings.PAGSEGURO["email"],
                                                     settings.PAGSEGURO["token"])
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

    def transaction_done(self, subscription_id):
        transaction = Transaction.objects.get(subscription_id=subscription_id)
        transaction.status = "done"
        transaction.save()
        context = {"profile": AccountProfile.objects.get(user=transaction.subscription.user),
                   "subscription": transaction.subscription}
        body = render_to_string("email_successful_registration.txt", context)
        subject = "PythonBrasil[8] - Registration Confirmation"
        mail.send(settings.EMAIL_SENDER,
                  transaction.subscription.user.email,
                  subject,
                  body)


    def transaction_canceled(self, subscription_id):
        transaction = Transaction.objects.get(subscription_id=subscription_id)
        transaction.status = "canceled"
        transaction.save()
        context = {"profile": AccountProfile.objects.get(user=transaction.subscription.user),
                   "subscription": transaction.subscription}
        body = render_to_string("email_unsuccessful_registration.txt", context)
        subject = "PythonBrasil[8] - Registration Confirmation"
        mail.send(settings.EMAIL_SENDER,
                  transaction.subscription.user.email,
                  subject,
                  body)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NotificationView, self).dispatch(*args, **kwargs)

    def post(self, request):
        notification_code = request.POST.get("notificationCode")

        if notification_code:
            status, subscription_id = self.transaction(notification_code)
            method = self.methods_by_status.get(status)

            if method:
                method(subscription_id)

        return HttpResponse("OK")
