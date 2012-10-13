# -*- coding: utf-8 -*-

from django.contrib import admin as django_admin
from django.contrib.auth import models as auth_models
from django.core import management
from django.test import TestCase

from pythonbrasil8.dashboard import models as dashboard_models
from pythonbrasil8.schedule import admin, models


class SessionAdminTestCase(TestCase):

    def test_Session_should_be_registered(self):
        self.assertIn(models.Session, django_admin.site._registry)

    def test_Session_should_be_registered_with_SessionAdmin(self):
        self.assertIsInstance(django_admin.site._registry[models.Session],
                              admin.SessionAdmin)

    def test_should_display_the_title(self):
        self.assertIn("title", admin.SessionAdmin.list_display)

    def test_should_display_the_type(self):
        self.assertIn("type", admin.SessionAdmin.list_display)

    def test_should_display_speakers(self):
        self.assertIn("speaker_names", admin.SessionAdmin.list_display)

    def test_should_display_the_track(self):
        self.assertIn("track", admin.SessionAdmin.list_display)

    def test_should_display_the_status(self):
        self.assertIn("status", admin.SessionAdmin.list_display)

    def test_should_be_able_to_filter_by_type(self):
        self.assertIn("type", admin.SessionAdmin.list_filter)

    def test_should_be_able_to_filter_by_status(self):
        self.assertIn("status", admin.SessionAdmin.list_filter)

    def test_speaker_names_should_return_the_name_of_the_speakers(self):
        user1, _ = auth_models.User.objects.get_or_create(username="foo",
                                                          email="foo@bar.com")
        dashboard_models.AccountProfile.objects.create(user=user1)
        user2, _ = auth_models.User.objects.get_or_create(username="foo2",
                                                          email="foo2@bar.com")
        dashboard_models.AccountProfile.objects.create(user=user2)
        user3, _ = auth_models.User.objects.get_or_create(username="foo3",
                                                          email="foo3@bar.com")
        dashboard_models.AccountProfile.objects.create(user=user3,
                                                       name="Foo Bar")
        track, _ = models.Track.objects.get_or_create(name_en_us="Session test",
                                                      description_en_us="test")
        session = models.Session.objects.create(
            title=u"Admin test",
            description=u"desc",
            type=u"admin_test",
            status=u"proposed",
            language=u"pt",
            track=track,
        )
        session.speakers = [user1, user2, user3]
        session.save()
        adm = admin.SessionAdmin(session, None)
        self.assertEqual("foo, foo2, Foo Bar", adm.speaker_names(session))

    def test_speaker_names_should_have_short_description(self):
        self.assertEqual(u"Speakers",
                         admin.SessionAdmin.speaker_names.short_description)
