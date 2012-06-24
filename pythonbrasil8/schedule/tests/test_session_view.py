# -*- coding: utf-8 -*-
from django import test
from django.contrib.auth import models as auth_models
from django.test import client

from pythonbrasil8.schedule import forms, models, views


class SessionViewTestCase(test.TestCase):

    def setUp(self):
        self.request = client.RequestFactory().get("/")
        self.request.user = auth_models.User()

    def tearDown(self):
        models.Session.objects.filter(title="some title").delete()
        models.Track.objects.filter(name_en_us="Session test").delete()

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

    def test_form_valid_saves_the_form_using_the_user_from_request(self):
        user, _ = auth_models.User.objects.get_or_create(username="foo")
        track = models.Track.objects.create(name="Session test", description="test")
        data = {
            "title": "some title",
            "description": "some description",
            "type": "talk",
            "tags": "some, tags",
            "track": track.pk,
            "language": "pt",
        }
        form = forms.SessionForm(data)
        request = client.RequestFactory().post("/", data)
        request.user = user
        v = views.SubscribeView(request=request)
        v.form_valid(form)
        s = models.Session.objects.get(title="some title")
        self.assertEqual(user, s.speakers.all()[0])

    def test_should_create_a_session_with_the_post_data_getting_user_from_request(self):
        user, _ = auth_models.User.objects.get_or_create(username="foo")
        track = models.Track.objects.create(name="Session test", description="test")
        data = {
            "title": "some title",
            "description": "some description",
            "type": "talk",
            "tags": "some, tags",
            "track": track.pk,
            "language": "pt",
        }
        request = client.RequestFactory().post("/", data)
        request.user = user
        result = views.SubscribeView.as_view()(request)
        self.assertEqual(302, result.status_code)
        session = models.Session.objects.get(title=data["title"])
        self.assertTrue(session.id)
        t = models.Session.objects.get(speakers=user)
        self.assertEqual(u"some title", t.title)
