from django.test import TestCase

from pythonbrasil8.dashboard.forms import ProfileForm
from pythonbrasil8.dashboard.models import AccountProfile


class ProfileFormTestCase(TestCase):

    def test_model_should_be_AccountProfile(self):
        self.assertEqual(AccountProfile, ProfileForm._meta.model)

    def test_field_user_should_be_exclude(self):
        self.assertIn('user', ProfileForm._meta.exclude)

    def test_field_payement_should_be_exclude(self):
        self.assertIn('payement', ProfileForm._meta.exclude)
