# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin

from pythonbrasil8.schedule import admin, models


class TrackAdminTestCase(unittest.TestCase):

    def test_should_be_registered(self):
        self.assertIn(models.Track, django_admin.site._registry)

    def test_should_be_registered_with_the_TrackAdmin_class(self):
        self.assertIsInstance(django_admin.site._registry[models.Track], admin.TrackAdmin)

    def test_should_display_the_name_of_the_track(self):
        self.assertIn("name", admin.TrackAdmin.list_display)
