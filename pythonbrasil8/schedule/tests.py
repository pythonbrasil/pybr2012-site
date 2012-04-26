from django.test import TestCase

from pythonbrasil8.schedule.models import Session


class SessionModelTestCase(TestCase):

    def test_should_have_title(self):
        self.assert_field_in('title', Session)

    def test_should_have_description(self):
        self.assert_field_in('description', Session)

    def test_should_have_tags(self):
        self.assert_field_in('tags', Session)

    def test_should_have_speakers(self):
        self.assert_field_in('speakers', Session)

    def test_should_have_type(self):
        self.assert_field_in('type', Session)

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())
