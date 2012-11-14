# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase

from pythonbrasil8.dashboard.forms import ProfileForm, SpeakerProfileForm
from pythonbrasil8.dashboard.models import AccountProfile


class ProfileFormTestCase(TestCase):

    def test_model_should_be_AccountProfile(self):
        self.assertEqual(AccountProfile, ProfileForm._meta.model)

    def test_field_user_should_be_exclude(self):
        self.assertIn('user', ProfileForm._meta.exclude)

    def test_field_payement_should_be_exclude(self):
        self.assertIn('payement', ProfileForm._meta.exclude)

    def test_should_use_TextArea_widget_for_description(self):
        self.assertEqual(forms.Textarea, ProfileForm.Meta.widgets['description'])


class SpeakerProfileFormTestCase(TestCase):

    def test_should_inherit_from_ProfileForm(self):
        assert issubclass(SpeakerProfileForm, ProfileForm)

    def test_Meta_should_inherit_from_ProfileForm_meta(self):
        assert issubclass(SpeakerProfileForm.Meta, ProfileForm.Meta)

    def test_should_exclude_everything_that_ProfileForm_excludes(self):
        for f in ProfileForm._meta.exclude:
            self.assertIn(f, SpeakerProfileForm._meta.exclude)

    def test_should_exclude_type(self):
        self.assertIn("type", SpeakerProfileForm._meta.exclude)
