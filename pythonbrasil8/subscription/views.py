# -*- coding: utf-8 -*-
import datetime
import re

import requests

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import response
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lxml import etree

from pythonbrasil8.core import mail
from pythonbrasil8.core.views import LoginRequiredMixin
from pythonbrasil8.dashboard.models import AccountProfile
from pythonbrasil8.schedule.models import Session
from pythonbrasil8.subscription.models import Subscription, Transaction


class SubscriptionView(LoginRequiredMixin, View):

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
        t = Transaction.generate(subscription)

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


class TutorialSubscriptionView(LoginRequiredMixin, View):

    def get(self, request):
        tutorials = Session.objects.filter(type="tutorial", status__in=["accepted", "confirmed"]).order_by("date")
        slots = []
        current_slot = None
        for tutorial in tutorials:
            if current_slot is None:
                current_slot = TutorialSlot([tutorial])
            elif tutorial.date == current_slot.date:
                current_slot.tutorials.append(tutorial)
            else:
                slots.append(current_slot)
                current_slot = TutorialSlot([tutorial])
        if current_slot:
            slots.append(current_slot)
        return response.TemplateResponse(
            request,
            "subscription/tutorials.html",
            context={"tutorials": slots},
        )

    def post(self, request):
        tutorials = []
        regexp = re.compile(r"tutorial-(\d{14})")
        for k, v in request.POST.iteritems():
            m = regexp.match(k)
            if m:
                tutorial = Session.objects.get(
                    pk=v,
                    date=datetime.datetime.strptime(m.groups()[0], "%Y%m%d%H%M%S"),
                    type="tutorial",
                )
                tutorials.append(tutorial)
        subscription = Subscription.objects.create(
            user=request.user,
            type="tutorial",
        )
        subscription.tutorials = tutorials
        subscription.save()
        transaction = Transaction.generate(subscription)
        return response.TemplateResponse(
            request,
            "subscription/tutorials_success.html",
            context={
                "transaction": transaction,
                "subscription": subscription,
            },
        )


class TutorialSlot(object):

    def __init__(self, tutorials):
        self.date = tutorials[0].date
        self.tutorials = tutorials


class NotificationView(View):

    def __init__(self, *args, **kwargs):
        self.methods_by_status = {
            3: self.transaction_done,
            4: self.transaction_done,
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
        transaction = Transaction.objects.select_related('subscription').get(subscription_id=subscription_id)
        transaction.status = "done"
        transaction.save()
        transaction.subscription.status = 'confirmed'
        transaction.subscription.save()
        context = {"profile": AccountProfile.objects.get(user=transaction.subscription.user),
  }
        body = render_to_string("email_successful_registration.txt", context)
        subject = "PythonBrasil[8] - Registration Confirmation"
        mail.send(settings.EMAIL_SENDER,
                  [transaction.subscription.user.email],
                  subject,
                  body)

    def transaction_canceled(self, subscription_id):
        transaction = Transaction.objects.get(subscription_id=subscription_id)
        transaction.status = "canceled"
        transaction.save()
        context = {"profile": AccountProfile.objects.get(user=transaction.subscription.user)}
        body = render_to_string("email_unsuccessful_registration.txt", context)
        subject = "PythonBrasil[8] - Registration Unsuccessful "
        mail.send(settings.EMAIL_SENDER,
                  [transaction.subscription.user.email],
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
