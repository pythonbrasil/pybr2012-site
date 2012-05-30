from django.db import models
from django.contrib.auth.models import User


PRICES = (
    ('student', 150),
    ('apyb', 150),
    ('individual', 250),
)


class Subscription(models.Model):

    TYPE = (
        ('tutorial', 'tutorial',),
        ('talk', 'talk'),
    )

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=25, choices=TYPE)

    def done(self):
        return self.transaction_set.filter(status="done").exists()


class Transaction(models.Model):
    subscription = models.ForeignKey("Subscription")
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=25)
