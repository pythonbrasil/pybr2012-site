# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db.models import CharField, ForeignKey, ManyToManyField

from pythonbrasil8.schedule.models import Session, Track


class SessionModelTestCase(TestCase):

    def test_should_have_title(self):
        self.assert_field_in("title", Session)

    def test_title_should_have_verbose_name(self):
        field = Session._meta.get_field_by_name("title")[0]
        self.assertEqual(u"Title", field.verbose_name)

    def test_should_have_description(self):
        self.assert_field_in("description", Session)

    def test_description_should_have_verbose_name(self):
        field = Session._meta.get_field_by_name("description")[0]
        self.assertEqual(u"Description", field.verbose_name)

    def test_should_have_speakers(self):
        self.assert_field_in("speakers", Session)

    def test_speakers_should_have_verbose_name(self):
        field = Session._meta.get_field_by_name("speakers")[0]
        self.assertEqual(u"Speakers", field.verbose_name)

    def test_should_have_type(self):
        self.assert_field_in("type", Session)

    def test_type_should_have_verbose_name(self):
        field = Session._meta.get_field_by_name("type")[0]
        self.assertEqual(u"Type", field.verbose_name)

    def test_type_should_have_choices(self):
        type_field = Session._meta.get_field_by_name("type")[0]
        choices = [choice[0] for choice in type_field._choices]
        self.assertIn("talk", choices)
        self.assertIn("tutorial", choices)

    def test_speakers_shoudl_be_a_ManyToManyField(self):
        speakers_field = Session._meta.get_field_by_name("speakers")[0]
        self.assertIsInstance(speakers_field, ManyToManyField)

    def test_should_have_a_foreign_key_to_track(self):
        self.assert_field_in("track", Session)
        field = Session._meta.get_field_by_name("track")[0]
        self.assertIsInstance(field, ForeignKey)

    def test_track_fk_should_point_to_Track_model(self):
        field = Session._meta.get_field_by_name("track")[0]
        self.assertEqual(Track, field.related.parent_model)

    def test_track_should_have_a_verbose_name(self):
        field = Session._meta.get_field_by_name("track")[0]
        self.assertEqual(u"Track", field.verbose_name)

    def test_should_have_a_language_field(self):
        self.assert_field_in("language", Session)

    def test_language_should_be_a_CharField(self):
        field = Session._meta.get_field_by_name("language")[0]
        self.assertIsInstance(field, CharField)

    def test_language_should_have_at_most_2_characters(self):
        field = Session._meta.get_field_by_name("language")[0]
        self.assertEqual(2, field.max_length)

    def test_language_should_have_three_options_en_es_pt(self):
        expected = (
            ("pt", "Portuguese"),
            ("en", "English"),
            ("es", "Spanish"),
        )
        field = Session._meta.get_field_by_name("language")[0]
        self.assertEqual(expected, field.choices)

    def test_language_should_have_a_verbose_name(self):
        field = Session._meta.get_field_by_name("language")[0]
        self.assertEqual(u"Language", field.verbose_name)

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())
