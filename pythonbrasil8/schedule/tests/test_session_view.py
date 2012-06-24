# -*- coding: utf-8 -*-
from django import http, test
from django.contrib.auth import models as auth_models
from django.template.response import TemplateResponse
from django.test import client

from pythonbrasil8.schedule import forms, models, views


class SessionViewTestCase(test.TestCase):

    def setUp(self):
        self.request = client.RequestFactory().get("/")
        self.request.user = auth_models.User()

    def tearDown(self):
        models.Session.objects.filter(title="some title").delete()

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
        user, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        track, _ = models.Track.objects.get_or_create(name_en_us="Session test", description_en_us="test")
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
        user, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        track, _  = models.Track.objects.get_or_create(name_en_us="Session test", description_en_us="test")
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

    def test_should_save_the_current_user_and_extra_speakers(self):
        user1, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        user2, _ = auth_models.User.objects.get_or_create(username="foo2", email="foo2@bar.com")
        track, _ = models.Track.objects.get_or_create(name_en_us="Session test", description_en_us="test")
        data = {
            "title": "some title",
            "description": "some description",
            "type": "talk",
            "tags": "some, tags",
            "track": track.pk,
            "language": "pt",
            "extra_speakers": "foo2@bar.com",
        }
        request = client.RequestFactory().post("/", data)
        request.user = user1
        result = views.SubscribeView.as_view()(request)
        self.assertEqual(302, result.status_code)
        session = models.Session.objects.get(title=data["title"])
        self.assertTrue(session.id)
        t = models.Session.objects.get(speakers=user1)
        self.assertEqual(u"some title", t.title)
        self.assertEqual([user1, user2], list(t.speakers.all()))

    def test_should_keep_extra_speakers_in_the_context_if_the_form_validation_fails(self):
        user1, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        user2, _ = auth_models.User.objects.get_or_create(username="foo2", email="foo2@bar.com")
        data = {
            "title": "some title",
            "language": "pt",
            "extra_speakers": "foo2@bar.com",
        }
        request = client.RequestFactory().post("/", data)
        request.user = user1
        response = views.SubscribeView.as_view()(request)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(["foo2@bar.com"], response.context_data["extra_speakers"])

    def test_get_speakers_return_speakers_from_extra_speakers_parameter(self):
        user1, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        user2, _ = auth_models.User.objects.get_or_create(username="foo2", email="foo2@bar.com")
        user3, _ = auth_models.User.objects.get_or_create(username="foo3", email="foo3@bar.com")
        v = views.SubscribeView()
        v.request = client.RequestFactory().post("/", {})
        v.request.POST = http.QueryDict("extra_speakers=foo&extra_speakers=foo2&extra_speakers=foo3@bar.com")
        speakers = v.get_extra_speakers()
        self.assertEqual([user1, user2, user3], list(speakers))

    def test_get_speakers_return_speakers_from_extra_speakers_parameter_even_if_it_is_only_one(self):
        user1, _ = auth_models.User.objects.get_or_create(username="foo", email="foo@bar.com")
        user2, _ = auth_models.User.objects.get_or_create(username="foo2", email="foo2@bar.com")
        user3, _ = auth_models.User.objects.get_or_create(username="foo3", email="foo3@bar.com")
        v = views.SubscribeView()
        v.request = client.RequestFactory().post("/", {"extra_speakers": "foo2@bar.com"})
        speakers = v.get_extra_speakers()
        self.assertEqual([user2], list(speakers))

    def test_get_speakers_return_empty_list_if_extra_speakers_is_missing(self):
        v = views.SubscribeView()
        v.request = client.RequestFactory().post("/", {})
        speakers = v.get_extra_speakers()
        self.assertEqual([], list(speakers))
