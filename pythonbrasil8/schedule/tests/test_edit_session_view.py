# -*- coding: utf-8 -*-
import unittest

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
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        resp = views.EditSessionView().get(request, 1)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual(views.EditSessionView.template_name, resp.template_name)
        self.assertIsInstance(resp.context_data["session"], models.Session)
        self.assertEqual(1, resp.context_data["session"].pk)

    def test_get_render_the_form_with_data_populated(self):
        instance = models.Session.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        resp = views.EditSessionView().get(request, 1)
        form = resp.context_data["form"]
        self.assertIsInstance(form, views.EditSessionView.form_class)
        self.assertEqual(instance, form.instance)

    def test_get_include_list_of_tracks_in_the_context(self):
        track = models.Track.objects.get(pk=1)
        request = client.RequestFactory().get("/dashboard/proposals/1/")
        resp = views.EditSessionView().get(request, 1)
        self.assertEqual([track], list(resp.context_data["tracks"]))
