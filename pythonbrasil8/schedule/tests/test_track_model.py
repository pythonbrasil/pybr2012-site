# -*- coding: utf-8 -*-
import unittest

import transmeta

from django.db import models as django_models

from pythonbrasil8.schedule import models


class TrackModelTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fields = {}
        for name in models.Track._meta.get_all_field_names():
            cls.fields[name] = models.Track._meta.get_field_by_name(name)[0]

    def test_should_use_TransMeta_as_metaclass(self):
        self.assertIsInstance(models.Track, transmeta.TransMeta)

    def test_should_have_a_name_field(self):
        self.assertIn("name_en_us", self.fields)
        self.assertIn("name_pt_br", self.fields)

    def test_name_should_be_a_CharField(self):
        field = self.fields["name_en_us"]
        self.assertIsInstance(field, django_models.CharField)

    def test_name_should_have_at_most_255_characters(self):
        field = self.fields["name_en_us"]
        self.assertEqual(255, field.max_length)

    def test_should_translate_name(self):
        self.assertIn("name", models.Track._meta.translatable_fields)

    def test_should_have_a_description_field(self):
        self.assertIn("description_en_us", self.fields)
        self.assertIn("description_pt_br", self.fields)

    def test_description_should_be_a_CharField(self):
        field = self.fields["description_en_us"]
        self.assertIsInstance(field, django_models.CharField)

    def test_description_should_have_at_most_2000_characters(self):
        field = self.fields["description_en_us"]
        self.assertEqual(2000, field.max_length)

    def test_should_translate_description(self):
        self.assertIn("description", models.Track._meta.translatable_fields)
