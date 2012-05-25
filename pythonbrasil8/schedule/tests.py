from django.test import TestCase
from django.test.client import RequestFactory
from django.db.models import ManyToManyField
from django.contrib.auth.models import User

from pythonbrasil8.schedule.models import Session
from pythonbrasil8.schedule.forms import SessionForm
from pythonbrasil8.schedule.views import SubscribeView


class SessionModelTestCase(TestCase):

    def test_should_have_title(self):
        self.assert_field_in('title', Session)

    def test_should_have_description(self):
        self.assert_field_in('description', Session)

    def test_should_have_tags(self):
        self.assert_field_in('tags', Session)

    def test_should_have_speakers(self):
        self.assert_field_in('speakers', Session)

    def test_should_have_type(self):
        self.assert_field_in('type', Session)

    def test_type_should_have_choices(self):
        type_field = Session._meta.get_field_by_name('type')[0]
        choices = [choice[0] for choice in type_field._choices]
        self.assertIn('talk', choices)
        self.assertIn('tutorial', choices)

    def test_speakers_shoudl_be_a_ManyToManyField(self):
        speakers_field = Session._meta.get_field_by_name('speakers')[0]
        self.assertIsInstance(speakers_field, ManyToManyField)

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())


class SessionViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.user = User()

    def test_should_returns_200_when_accessed_by_get(self):
        result = SubscribeView.as_view()(self.request)
        self.assertEqual(200, result.status_code)

    def test_should_be_use_a_expected_template(self):
        result = SubscribeView.as_view()(self.request)
        self.assertEqual(['schedule/subscribe.html'], result.template_name)

    def test_should_be_form_in_context(self):
        result = SubscribeView.as_view()(self.request)
        self.assertIn('form', result.context_data)
        self.assertIsInstance(result.context_data['form'], SessionForm)

    def test_should_create_a_session_with_the_post_data(self):
        user = User.objects.create(username="foo")
        data = {
            "title": "some title",
            "description": "some description",
            "type": "talk",
            "tags": "some, tags",
            "speakers": user.id,
        }
        request = RequestFactory().post("/", data)
        request.user = User()
        result = SubscribeView.as_view()(request)
        self.assertEqual(302, result.status_code)
        session = Session.objects.get(title=data["title"])
        self.assertTrue(session.id)


class SessionFormTestCase(TestCase):

    def test_model_should_be_Session(self):
        self.assertEqual(Session, SessionForm._meta.model)
