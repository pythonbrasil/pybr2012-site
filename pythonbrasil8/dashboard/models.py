from django.db import models
from django.contrib.auth.models import User

from pythonbrasil8.dashboard import choices


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
