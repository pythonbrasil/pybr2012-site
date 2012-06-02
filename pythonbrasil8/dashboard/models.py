# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext

from pythonbrasil8.dashboard import choices

from registration.signals import user_activated


class AccountProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    type = models.CharField(max_length=50, choices=choices.ATTENDANT_CHOICES)
    tshirt = models.CharField(max_length=50, choices=choices.T_SHIRT_CHOICES)
    locale = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=choices.GENDER_CHOICES)
    age = models.CharField(max_length=20, null=True, blank=True, choices=choices.AGE_CHOICES)
    profession = models.CharField(max_length=50, null=True, blank=True, choices=choices.PROFESSION_CHOICES)
    institution = models.CharField(max_length=100, null=True, blank=True, verbose_name='Company / University / Institution')
    payement = models.BooleanField(default=False)
    twitter = models.CharField(max_length=15, blank=True, null=True, verbose_name=ugettext(u"Twitter profile"))
    public = models.BooleanField(default=True, verbose_name=ugettext(u"Public profile (visible to everyone)?"))

    def has_talk_subscription(self):
        return self.user.subscription_set.exists()

    def talk_subscription(self):
        return self.user.subscription_set.all()[0]


@receiver(user_activated)
def create_account_profile(user, request, *args, **kwargs):
    AccountProfile.objects.create(user=user)
