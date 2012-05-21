from django.test import TestCase
from django.test.client import RequestFactory
from django.db import models
from django.contrib.auth.models import User

from pythonbrasil8.subscription.models import Subscription, Transaction
from pythonbrasil8.subscription.views import SubscriptionView
from pythonbrasil8.subscription import views


class SubscriptionModelTestCase(TestCase):

    def test_should_have_type(self):
        self.assert_field_in('type', Subscription)

    def test_type_should_be_CharField(self):
        type_field = Subscription._meta.get_field_by_name('type')[0]
        self.assertIsInstance(type_field, models.CharField)

    def test_type_should_have_choices(self):
        type_field = Subscription._meta.get_field_by_name('type')[0]
        choices = [choice[0] for choice in type_field._choices]
        self.assertIn('talk', choices)
        self.assertIn('tutorial', choices)

    def test_should_have_user(self):
        self.assert_field_in('user', Subscription)

    def test_user_should_be_a_foreign_key(self):
        user_field = Subscription._meta.get_field_by_name('user')[0]
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertEqual(User, user_field.related.parent_model)

    def test_should_have_date(self):
        self.assert_field_in('date', Subscription)

    def test_date_should_be_datetime_field(self):
        date_field = Subscription._meta.get_field_by_name('date')[0]
        self.assertIsInstance(date_field, models.DateTimeField)
        self.assertTrue(date_field.auto_now_add)

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())


class TransacitonModelTestCase(TestCase):

    def test_should_have_code(self):
        self.assert_field_in('code', Transaction)

    def test_should_have_subscription(self):
        self.assert_field_in('subscription', Transaction)

        subscription_field = Transaction._meta.get_field_by_name('subscription')[0]
        self.assertIsInstance(subscription_field, models.ForeignKey)
        self.assertEqual(Subscription, subscription_field.related.parent_model)

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())


class SubscriptionViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Wolverine")
        self.request = RequestFactory().post("/", {})
        self.request.user = self.user

        self.requests_original = views.requests

        class ResponseMock(object):
            content = "<code>xpto123</code>"
            def ok(self):
                return True

        def post(self, *args, **kwargs):
            return ResponseMock()

        views.requests.post = post

    def tearDown(self):
        views.requests = self.requests_original

    def test_subscription_view_should_create_a_subscription_for_the_current_user(self):
        response = SubscriptionView.as_view()(self.request)
        self.assertTrue(Subscription.objects.filter(user=self.user).exists())
        self.assertEqual(200, response.status_code)
        self.assertEqual("subscription created with success!", response.content)

    def test_should_returns_error_when_user_is_not_logged(self):
        self.request.user = None
        response = SubscriptionView.as_view()(self.request)
        self.assertEqual(500, response.status_code)
        self.assertEqual("you should be logged in.", response.content)

    def test_generate_transaction(self):
        subscription = Subscription.objects.create(
            status='pending',
            type='talk',
           user=self.user,
        )
        transaction = SubscriptionView().generate_transaction(subscription)
        self.assertEqual(subscription, transaction.subscription)
        self.assertEqual("xpto123", transaction.code)
