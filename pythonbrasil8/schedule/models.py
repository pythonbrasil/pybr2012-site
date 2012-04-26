from django.db import models

from django.contrib.auth.models import User


class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=1)
    tags = models.CharField(max_length=255)
    speakers = models.ForeignKey(User)
