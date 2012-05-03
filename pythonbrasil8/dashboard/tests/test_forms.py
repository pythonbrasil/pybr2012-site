from django.test import TestCase

from pythonbrasil8.dashboard.forms import ProfileForm
from pythonbrasil8.dashboard.models import AccountProfile


class ProfileFormTestCase(TestCase):

    def test_model_should_be_AccountProfile(self):
        self.assertEqual(AccountProfile, ProfileForm._meta.model)
