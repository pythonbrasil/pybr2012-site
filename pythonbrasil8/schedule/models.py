from django.db import models

from django.contrib.auth.models import User


class Session(models.Model):

    TYPE = (
        ('tutorial', 'tutorial',),
        ('talk', 'talk'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE)
    tags = models.CharField(max_length=255)
    speakers = models.ForeignKey(User)
