from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):

    TYPE = (
        ('tutorial', 'tutorial',),
        ('talk', 'talk'),
    )

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=25, choices=TYPE)


class Transaction(models.Model):
    subscription = models.ForeignKey("Subscription")
    code = models.CharField(max_length=50)
