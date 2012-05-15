from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from pythonbrasil8.dashboard.models import AccountProfile

from registration.signals import user_activated


class AccountTestCase(TestCase):

    def test_should_create_a_userprofile_when_user_is_activated(self):
        user = User.objects.create(username="ironman")
        request = RequestFactory().get("/")
        user_activated.send(sender=self.__class__, user=user, request=request)
        self.assertTrue(AccountProfile.objects.filter(user=user).exists())
