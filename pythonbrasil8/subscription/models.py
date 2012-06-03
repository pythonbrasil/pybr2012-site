from django.db import models
from django.contrib.auth.models import User

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

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=25, choices=TYPE)

    def done(self):
        return self.transaction_set.filter(status="done").exists()


class Transaction(models.Model):
    subscription = models.ForeignKey("Subscription")
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2)
