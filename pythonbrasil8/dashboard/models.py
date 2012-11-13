# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models as django_models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy

from pythonbrasil8.dashboard import choices
from pythonbrasil8.subscription import models
from registration.signals import user_activated


class CompleteSubscriptionException(Exception):
    pass


class AccountProfile(django_models.Model):
    user = django_models.OneToOneField(User)
    name = django_models.CharField(max_length=20, verbose_name=ugettext_lazy(u"Name"))
    description = django_models.CharField(max_length=500, verbose_name=ugettext_lazy(u"Short Bio"))
    type = django_models.CharField(max_length=50, choices=choices.ATTENDANT_CHOICES, verbose_name=ugettext_lazy(u"Registration type"))
    tshirt = django_models.CharField(max_length=50, choices=choices.T_SHIRT_CHOICES, verbose_name=ugettext_lazy(u"T-Shirt size"))
    locale = django_models.CharField(max_length=255, choices=choices.LOCALE_CHOICES, verbose_name=ugettext_lazy(u"State"))
    country = django_models.CharField(max_length=50, null=True, blank=True, verbose_name=ugettext_lazy(u"Country (if not Brazilian)"))
    gender = django_models.CharField(max_length=20, choices=choices.GENDER_CHOICES, verbose_name=ugettext_lazy(u"Gender"))
    age = django_models.CharField(max_length=20, null=True, blank=True, choices=choices.AGE_CHOICES, verbose_name=ugettext_lazy(u"Age"))
    profession = django_models.CharField(max_length=50, null=True, blank=True, choices=choices.PROFESSION_CHOICES, verbose_name=ugettext_lazy(u"Profession"))
    institution = django_models.CharField(max_length=100, null=True, blank=True, verbose_name=ugettext_lazy(u"Company / University / Institution"))
    payement = django_models.BooleanField(default=False)
    twitter = django_models.CharField(max_length=15, blank=True, null=True, verbose_name=ugettext_lazy(u"Twitter profile"))
    public = django_models.BooleanField(default=True, verbose_name=ugettext_lazy(u"Public profile (visible to everyone)?"))

    def has_talk_subscription(self):
        return self.user.subscription_set.filter(type="talk").exists()

    def talk_subscription(self):
        return self.user.subscription_set.filter(type="talk")[0]

    @property
    def transaction(self):
        subscription = None
        if self.has_talk_subscription():
            subscription = self.talk_subscription()
            if subscription.done():
                raise CompleteSubscriptionException("This subscription is complete.")
            qs = subscription.transaction_set.filter(
                price=models.PRICES[self.type],
                status="pending",
            )
            if qs:
                return qs[0]
        if not subscription:
            subscription = models.Subscription.objects.create(
                user=self.user,
                type="talk",
            )
        subscription.transaction_set.update(status="canceled")
        return models.Transaction.generate(subscription)


@receiver(user_activated)
def create_account_profile(user, request, *args, **kwargs):
    AccountProfile.objects.create(user=user)
