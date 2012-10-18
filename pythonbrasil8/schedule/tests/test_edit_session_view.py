# -*- coding: utf-8 -*-
import unittest

from django import http
from django.contrib.auth import models as auth_models
from django.core import management
from django.template import response
from django.test import client

from pythonbrasil8.schedule import forms, models, views


class EditSessionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "sessions.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_should_use_SessionForm_as_form_class(self):
        self.assertEqual(forms.SessionForm, views.EditSessionView.form_class)

    def test_template_name_should_be_edit_session_html(self):
        self.assertEqual("schedule/edit-session.html", views.EditSessionView.template_name)

    def test_get_render_the_template_with_the_session_in_context(self):
        instance = models.Session.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        request.user = instance.speakers.get(username="chico")
        resp = views.EditSessionView().get(request, 1)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual(views.EditSessionView.template_name, resp.template_name)
        self.assertIsInstance(resp.context_data["session"], models.Session)
        self.assertEqual(1, resp.context_data["session"].pk)

    def test_get_render_the_form_with_data_populated(self):
        instance = models.Session.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        request.user = instance.speakers.get(username="chico")
        resp = views.EditSessionView().get(request, 1)
        form = resp.context_data["form"]
        self.assertIsInstance(form, views.EditSessionView.form_class)
        self.assertEqual(instance, form.instance)

    def test_get_return_404_if_the_user_is_not_speaker_in_the_talk(self):
        user, _ = auth_models.User.objects.get_or_create(username="aidimim")
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        request.user = user
        with self.assertRaises(http.Http404):
            views.EditSessionView().get(request, 1)

    def test_get_include_list_of_tracks_in_the_context(self):
        track = models.Track.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        request.user = models.Session.objects.get(pk=1).speakers.get(username="chico")
        resp = views.EditSessionView().get(request, 1)
        self.assertEqual(track, list(resp.context_data["tracks"])[0])

    def test_post_updates_the_session(self):
        instance = models.Session.objects.get(pk=1)
        data = {
            "title": instance.title + " updated",
            "description": instance.description,
            "type": "talk",
            "audience_level": "intermediate",
            "tags": "some, tags",
            "track": instance.track.pk,
            "language": "en",
        }
        request = client.RequestFactory().post("/dashboard/proposals/1/", data)
        request.user = instance.speakers.get(username="chico")
        resp = views.EditSessionView().post(request, 1)
        self.assertIsInstance(resp, http.HttpResponseRedirect)
        self.assertEqual("/dashboard/proposals/", resp["Location"])
        instance = models.Session.objects.get(pk=1)
        self.assertEqual(data["title"], instance.title)

    def test_post_renders_template_name_with_form_and_tracks_in_context(self):
        instance = models.Session.objects.get(pk=1)
        data = {
            "type": "talk",
            "audience_level": "advanced",
            "tags": "some, tags",
            "track": instance.track.pk,
            "language": "en",
        }
        request = client.RequestFactory().post("/dashboard/proposals/1/", data)
        request.user = instance.speakers.get(username="chico")
        resp = views.EditSessionView().post(request, 1)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual(views.EditSessionView.template_name, resp.template_name)
        self.assertEqual(instance.track, list(resp.context_data["tracks"])[0])
        form = resp.context_data["form"]
        self.assertIsInstance(form, views.EditSessionView.form_class)
        self.assertEqual(data["audience_level"], form.data["audience_level"])

    def test_get_render_the_template_with_extra_speakers_in_context(self):
        instance = models.Session.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/2/")
        request.user = instance.speakers.get(username="chico")
        result = views.EditSessionView().get(request, 2)
        self.assertIn('extra_speakers', result.context_data)
        self.assertEqual(result.context_data["extra_speakers"][0].pk, 2)