# -*- coding: utf-8 -*-
import unittest

from django.contrib import admin as django_admin

from pythonbrasil8.schedule import admin, models


class SessionAdminTestCase(unittest.TestCase):

    def test_Session_should_be_registered(self):
        self.assertIn(models.Session, django_admin.site._registry)

    def test_Session_should_be_registered_with_SessionAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Session], admin.SessionAdmin)

    def test_should_display_the_title(self):
        self.assertIn("title", admin.SessionAdmin.list_display)

    def test_should_display_the_description(self):
        self.assertIn("description", admin.SessionAdmin.list_display)

    def test_should_display_the_type(self):
        self.assertIn("type", admin.SessionAdmin.list_display)

    def test_should_be_able_to_filter_by_type(self):
        self.assertIn("type", admin.SessionAdmin.list_filter)
