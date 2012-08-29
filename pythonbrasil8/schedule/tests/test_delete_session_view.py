# -*- coding: utf-8 -*-
import unittest

from django import http
from django.contrib.auth import models as auth_models
from django.core import management
from django.test import client

from pythonbrasil8.schedule import models, views


class DeleteSessionViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "sessions.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_get_deletes_the_proposal(self):
        request = client.RequestFactory().get("/dashboard/proposals/delete/1/")
        request.user = models.Session.objects.get(pk=1).speakers.get(username="chico")
        resp = views.DeleteSessionView().get(request, 1)
        self.assertIsInstance(resp, http.HttpResponseRedirect)
        self.assertEqual("/dashboard/proposals/", resp["Location"])
        with self.assertRaises(models.Session.DoesNotExist):
            models.Session.objects.get(pk=1)

    def test_get_return_404_if_the_user_is_not_speaker_in_the_talk(self):
        user, _ = auth_models.User.objects.get_or_create(username="aidimim")
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        request.user = user
        with self.assertRaises(http.Http404):
            views.DeleteSessionView().get(request, 1)
