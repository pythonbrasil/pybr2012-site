from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from pythonbrasil8.subscription.models import Subscription, Transaction


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
