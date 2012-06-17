# -*- coding: utf-8 -*-
from django import test
from django.contrib.auth import models as auth_models
from django.test import client

from pythonbrasil8.schedule import forms, models, views


class SessionViewTestCase(test.TestCase):

    def setUp(self):
        self.request = client.RequestFactory().get("/")
        self.request.user = auth_models.User()

    def test_should_returns_200_when_accessed_by_get(self):
        result = views.SubscribeView.as_view()(self.request)
        self.assertEqual(200, result.status_code)

    def test_should_be_use_a_expected_template(self):
        result = views.SubscribeView.as_view()(self.request)
        self.assertEqual(['schedule/subscribe.html'], result.template_name)

    def test_should_be_form_in_context(self):
        result = views.SubscribeView.as_view()(self.request)
        self.assertIn('form', result.context_data)
        self.assertIsInstance(result.context_data['form'], forms.SessionForm)

    def test_should_create_a_session_with_the_post_data(self):
        user = auth_models.User.objects.create(username="foo")
        data = {
            "title": "some title",
            "description": "some description",
            "type": "talk",
            "tags": "some, tags",
            "speakers": user.id,
        }
        request = client.RequestFactory().post("/", data)
        request.user = auth_models.User()
        result = views.SubscribeView.as_view()(request)
        self.assertEqual(302, result.status_code)
        session = models.Session.objects.get(title=data["title"])
        self.assertTrue(session.id)
