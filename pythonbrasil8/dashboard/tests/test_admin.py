# -*- coding: utf-8 -*-
from django import test
from django.contrib import admin as django_admin

from pythonbrasil8.dashboard import admin, models


class AccountProfileAdminTestCase(test.TestCase):

    def test_AccountProfile_is_registered(self):
        self.assertIn(models.AccountProfile, django_admin.site._registry)

    def test_AccountProfile_is_registered_with_AccountProfileAdmin(self):
        self.assertIsInstance(
            django_admin.site._registry[models.AccountProfile],
            admin.AccountProfileAdmin,
        )

    def test_name_is_displayed(self):
        self.assertIn("name", admin.AccountProfileAdmin.list_display)

    def test_user_is_displayed(self):
        self.assertIn("user", admin.AccountProfileAdmin.list_display)

    def test_name_is_used_for_search(self):
        self.assertIn("name", admin.AccountProfileAdmin.search_fields)

    def test_type_is_used_for_filtering(self):
        self.assertIn("type", admin.AccountProfileAdmin.list_filter)
