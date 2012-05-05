from django.test import TestCase

from pythonbrasil8.dashboard.forms import AddUserForm
from pythonbrasil8.dashboard.models import AccoutProfile


class AddUserFormTestCase(TestCase):

    def test_forms_model_should_be_User(self):
        self.assertEquals(AccoutProfile, AddUserForm.Meta.model)
