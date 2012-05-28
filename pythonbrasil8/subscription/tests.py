from django.test import TestCase
from django.test.client import RequestFactory
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch

from pythonbrasil8.subscription.models import Subscription, Transaction
from pythonbrasil8.subscription.views import SubscriptionView, NotificationView
from pythonbrasil8.subscription import views


class SubscriptionModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Wolverine")

    def test_name_url(self):
        try:
            reverse('talk-subscription')
        except NoReverseMatch:
            self.fail("Reversal of url named 'talk-subscription' failed with NoReverseMatch")

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

    def test_subscription_done_should_be_false_if_has_not_a_transaction(self):
        self.assertFalse(Subscription().done())

    def test_subscription_done_should_be_false_if_transactions_isnt_done(self):
        subscription = Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        Transaction.objects.create(
            subscription=subscription,
            status="pending",
            code="xpto",
        )
        self.assertFalse(subscription.done())

    def test_subscription_done_should_be_truth_if_transactions_is_done(self):
        subscription = Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        Transaction.objects.create(
            subscription=subscription,
            status="done",
            code="xpto",
        )
        self.assertTrue(subscription.done())
    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())


class TransacitonModelTestCase(TestCase):

    def test_should_have_code(self):
        self.assert_field_in('code', Transaction)

    def test_should_have_status(self):
        self.assert_field_in('status', Transaction)

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
        self.request = RequestFactory().get("/", {})
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
        self.assertEqual(302, response.status_code)
        self.assertEqual("/dashboard/", response.items()[1][1])

    def test_should_returns_error_when_user_is_not_logged(self):
        self.request.user.is_authenticated = lambda : False
        response = SubscriptionView.as_view()(self.request)
        self.assertEqual(302, response.status_code)
        self.assertIn('/accounts/login/', response.items()[1][1])

    def test_generate_transaction(self):
        subscription = Subscription.objects.create(
            type='talk',
            user=self.user,
        )
        transaction = SubscriptionView().generate_transaction(subscription)
        self.assertEqual(subscription, transaction.subscription)
        self.assertEqual("xpto123", transaction.code)


class NotificationViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Wolverine")
        self.requests_original = views.requests

        class ResponseMock(object):
            content = "<xml><status>3</status><reference>3</reference></xml>"
            def ok(self):
                return True

        def get(self, *args, **kwargs):
            return ResponseMock()

        views.requests.get = get

    def tearDown(self):
        views.requests = self.requests_original

    def test_name_url(self):
        try:
            reverse('notification')
        except NoReverseMatch:
            self.fail("Reversal of url named 'notification' failed with NoReverseMatch")

    def test_transaction_should_get_info_about_transaction(self):
        status, ref = NotificationView().transaction("code")
        self.assertEqual(3, status)
        self.assertEqual(3, ref)

    def test_transaction_done(self):
        subscription = Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        transaction = Transaction.objects.create(
            subscription=subscription,
            status="pending",
            code="xpto",
        )
        NotificationView().transaction_done(subscription.id)
        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("done", transaction.status)

    def test_transaction_canceled(self):
        subscription = Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        transaction = Transaction.objects.create(
            subscription=subscription,
            status="pending",
            code="xpto",
        )
        NotificationView().transaction_canceled(subscription.id)
        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("canceled", transaction.status)

    def test_methods_by_status(self):
        methods_by_status = NotificationView().methods_by_status
        self.assertEqual("transaction_done", methods_by_status[3].__name__)
        self.assertEqual("transaction_canceled", methods_by_status[7].__name__)

    def test_post(self):
        subscription = Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        transaction = Transaction.objects.create(
            subscription=subscription,
            status="pending",
            code="xpto",
        )
        notification_view = NotificationView()
        notification_view.transaction = (lambda code: (3, 1))
        request = RequestFactory().post("/", {"notificationCode": "123"})

        response = notification_view.post(request)

        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("done", transaction.status)
        self.assertEqual("OK", response.content)
