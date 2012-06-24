# -*- coding: utf-8 -*-
from django import test

from pythonbrasil8.schedule import forms, models


class SessionFormTestCase(test.TestCase):

    def test_model_should_be_Session(self):
        self.assertEqual(models.Session, forms.SessionForm._meta.model)

    def test_should_exclude_speakers_field(self):
        self.assertIn("speakers", forms.SessionForm._meta.exclude)

    def test_should_exclude_status_field(self):
        self.assertIn("status", forms.SessionForm._meta.exclude)
