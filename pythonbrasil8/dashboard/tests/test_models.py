# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core import management
from django.db import models as django_models
from django.test import TestCase

from pythonbrasil8.dashboard.models import AccountProfile, CompleteSubscriptionException
from pythonbrasil8.subscription import models


class AccountProfileTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        self.field_names = AccountProfile._meta.get_all_field_names()

    def test_should_have_user_field(self):
        self.assertIn('user', self.field_names)

    def test_user_field_should_be_one_to_one_field(self):
        field = AccountProfile._meta.get_field_by_name('user')[0]
        self.assertEqual(django_models.OneToOneField, field.__class__)

    def test_should_have_name(self):
        self.assertIn('name', self.field_names)

    def test_name_should_be_CharField(self):
        field = AccountProfile._meta.get_field_by_name('name')[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_name_should_have_at_most_20_characters(self):
        field = AccountProfile._meta.get_field_by_name('name')[0]
        self.assertEqual(20, field.max_length)

    def test_name_should_have_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('name')[0]
        self.assertEqual(u"Name", field.verbose_name)

    def test_should_have_description_field(self):
        self.assertIn('description', self.field_names)

    def test_description_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('description')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_description_field_should_have_500_of_max_length(self):
        field = AccountProfile._meta.get_field_by_name('description')[0]
        self.assertEqual(500, field.max_length)

    def test_should_have_type_field(self):
        self.assertIn('type', self.field_names)

    def test_type_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('type')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_type_field_should_have_expected_choices(self):
        field = AccountProfile._meta.get_field_by_name('type')[0]
        self.assertIn(('Student', 'Student'), field.choices)
        self.assertIn(('APyB Associated', 'APyB Associated'), field.choices)
        self.assertIn(('Individual', 'Individual'), field.choices)

    def test_type_should_have_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('type')[0]
        self.assertEqual(u"Registration type", field.verbose_name)

    def test_should_have_tshirt_field(self):
        self.assertIn('tshirt', self.field_names)

    def test_tshirt_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('tshirt')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_tshirt_field_should_have_expected_choices(self):
        field = AccountProfile._meta.get_field_by_name('tshirt')[0]
        female_choices = (
            'Female', (
                ('S', 'S'),
                ('M', 'M'),
                ('L', 'L'),
            )
        )
        male_choices = (
            'Male', (
                ('S', 'S'),
                ('M', 'M'),
                ('L', 'L'),
                ('XL', 'XL'),
                ('XXL', 'XXL'),
            )
        )

        self.assertIn(female_choices, field.choices)
        self.assertIn(male_choices, field.choices)

    def test_tshirt_field_should_have_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('tshirt')[0]
        self.assertEqual(u"T-Shirt size", field.verbose_name)

    def test_should_have_locale_field(self):
        self.assertIn('locale', self.field_names)

    def test_locale_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('locale')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_locale_field_should_have_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('locale')[0]
        self.assertEqual(u"State", field.verbose_name)

    def test_locale_field_should_have_brazilian_states_choices(self):
        expected = (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AM', 'Amazonas'),
            ('AP', 'Amapá'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MS', 'Mato Grosso do Sul'),
            ('MT', 'Mato Grosso'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('PR', 'Paraná'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('RS', 'Rio Grande do Sul'),
            ('SC', 'Santa Catarina'),
            ('SE', 'Sergipe'),
            ('SP', 'São Paulo'),
            ('TO', 'Tocantins'),
            ('00', 'Other country')
        )
        field = AccountProfile._meta.get_field_by_name('locale')[0]
        self.assertEqual(expected, field.choices)

    def test_should_have_country_field(self):
        self.assertIn('country', self.field_names)

    def test_gender_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('country')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_should_have_gender_field(self):
        self.assertIn('gender', self.field_names)

    def test_gender_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('gender')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_gender_field_should_have_expected_choices(self):
        field = AccountProfile._meta.get_field_by_name('gender')[0]
        self.assertIn(('female', 'Female'), field.choices)
        self.assertIn(('male', 'Male'), field.choices)
        self.assertIn(('other', 'Other'), field.choices)

    def test_gender_should_have_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('gender')[0]
        self.assertEqual(u"Gender", field.verbose_name)

    def test_should_have_age_field(self):
        self.assertIn('age', self.field_names)

    def test_age_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('age')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_age_field_should_have_expected_choices(self):
        field = AccountProfile._meta.get_field_by_name('age')[0]
        self.assertIn(('--9', '9 or less'), field.choices)
        self.assertIn(('10-19', '10-19'), field.choices)
        self.assertIn(('20-29', '20-29'), field.choices)
        self.assertIn(('30-39', '30-39'), field.choices)
        self.assertIn(('40-49', '40-49'), field.choices)
        self.assertIn(('50-59', '50-59'), field.choices)
        self.assertIn(('60-69', '60-69'), field.choices)
        self.assertIn(('70-79', '70-79'), field.choices)
        self.assertIn(('80-+', '80 or more'), field.choices)

    def test_age_field_should_be_optional(self):
        field = AccountProfile._meta.get_field_by_name('age')[0]
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_age_should_have_a_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('age')[0]
        self.assertEqual(u"Age", field.verbose_name)

    def test_should_have_profession_field(self):
        self.assertIn('profession', self.field_names)

    def test_profession_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('profession')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_profession_field_should_have_expected_choices(self):
        field = AccountProfile._meta.get_field_by_name('profession')[0]
        self.assertIn(('student', 'Student'), field.choices)
        self.assertIn(('trainee', 'Trainee'), field.choices)
        self.assertIn(('developer', 'Developer'), field.choices)
        self.assertIn(('software engineer', 'Software engineer'), field.choices)
        self.assertIn(('manager', 'Manager'), field.choices)
        self.assertIn(('sysadmin', 'Sysadmin'), field.choices)
        self.assertIn(('teacher', 'Teacher'), field.choices)
        self.assertIn(('other', 'Other'), field.choices)

    def test_profession_field_should_be_optional(self):
        field = AccountProfile._meta.get_field_by_name('profession')[0]
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_profession_should_have_a_verbose_name(self):
        field = AccountProfile._meta.get_field_by_name('profession')[0]
        self.assertEqual(u"Profession", field.verbose_name)

    def test_should_have_institution_field(self):
        self.assertIn('institution', self.field_names)

    def test_institution_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('institution')[0]
        self.assertEqual(django_models.CharField, field.__class__)

    def test_institution_field_should_be_optional(self):
        field = AccountProfile._meta.get_field_by_name('institution')[0]
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_institution_field_should_have_verbose_name_company_university_institution(self):
        field = AccountProfile._meta.get_field_by_name('institution')[0]
        self.assertEquals('Company / University / Institution', field.verbose_name)

    def test_should_have_payement_field(self):
        self.assertIn('payement', self.field_names)

    def test_payement_field_should_be_char_field(self):
        field = AccountProfile._meta.get_field_by_name('payement')[0]
        self.assertEqual(django_models.BooleanField, field.__class__)

    def test_payement_field_should_have_default_False(self):
        field = AccountProfile._meta.get_field_by_name('payement')[0]
        self.assertFalse(field.default)

    def test_have_talk_subscription_should_be_false_when_use_hasnt_a_subscription(self):
        user = User.objects.create(username="tony")
        profile = AccountProfile.objects.create(user=user)
        self.assertFalse(profile.has_talk_subscription())

    def test_have_talk_subscription_shoud_be_true_when_user_has_a_subscription(self):
        user = User.objects.create(username="tony")
        profile = AccountProfile.objects.create(user=user)
        models.Subscription.objects.create(user=user, type="talk")
        self.assertTrue(profile.has_talk_subscription())

    def test_talk_subscription_shoud_be_returns_the_talk_subscription(self):
        user = User.objects.create(username="tony")
        profile = AccountProfile.objects.create(user=user)
        subscription = models.Subscription.objects.create(user=user, type="talk")
        self.assertEqual(subscription, profile.talk_subscription())

    def test_should_have_twitter_field(self):
        self.assertIn('twitter', self.field_names)

    def test_twitter_should_be_a_CharField(self):
        f = AccountProfile._meta.get_field_by_name('twitter')[0]
        self.assertIsInstance(f, django_models.CharField)

    def test_twitter_should_have_at_most_15_characters(self):
        f = AccountProfile._meta.get_field_by_name('twitter')[0]
        self.assertEqual(15, f.max_length)

    def test_twitter_should_accept_blank(self):
        f = AccountProfile._meta.get_field_by_name('twitter')[0]
        self.assertTrue(f.blank)

    def test_twitter_should_be_nullable(self):
        f = AccountProfile._meta.get_field_by_name('twitter')[0]
        self.assertTrue(f.null)

    def test_twitter_should_have_verbose_name(self):
        f = AccountProfile._meta.get_field_by_name('twitter')[0]
        self.assertEqual(u"Twitter profile", f.verbose_name)

    def test_should_have_field_for_public_displayable(self):
        self.assertIn('public', self.field_names)

    def test_public_should_be_a_BooleanField(self):
        f = AccountProfile._meta.get_field_by_name('public')[0]
        self.assertIsInstance(f, django_models.BooleanField)

    def test_public_should_be_true_by_default(self):
        f = AccountProfile._meta.get_field_by_name('public')[0]
        self.assertEqual(True, f.default)

    def test_public_should_have_verbose_name(self):
        f = AccountProfile._meta.get_field_by_name('public')[0]
        self.assertEqual(u"Public profile (visible to everyone)?", f.verbose_name)


class AccountProfileTransactionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "profiles.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def tearDown(self):
        if hasattr(self, "requests_original"):
            models.request = self.requests_original

    def _mock_requests(self, body, ok):
        self.requests_original = models.requests

        class ResponseMock(object):
            content = body

            def ok(self):
                return False

        def post(self, *args, **kwargs):
            return ResponseMock()

        models.requests.post = post

    def test_transaction_returns_a_new_transaction_if_the_profile_does_not_have_one(self):
        profile = self.user.get_profile()
        self._mock_requests("<code>xpto1234</code>", True)
        transaction = profile.transaction
        self.assertEqual(models.PRICES[profile.type], transaction.price)
        self.assertEqual("xpto1234", transaction.code)

    def test_transaction_raises_exception_if_the_user_has_a_done_subscription(self):
        subscription = models.Subscription.objects.create(
            user=self.user,
            type="talk",
            status="sponsor",
        )
        try:
            with self.assertRaises(CompleteSubscriptionException) as cm:
                self.user.get_profile().transaction
            exc = cm.exception
            self.assertEqual("This subscription is complete.", exc.args[0])
        finally:
            subscription.delete()

    def test_transaction_returns_the_already_created_transaction_if_it_matches_the_price(self):
        subscription = models.Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        profile = self.user.get_profile()
        transaction = models.Transaction.objects.create(
            subscription=subscription,
            price=models.PRICES[profile.type],
            code="abcd123",
            status="pending",
        )
        try:
            got_transaction = profile.transaction
            self.assertEqual(transaction.pk, got_transaction.pk)
        finally:
            transaction.delete()
            subscription.delete()

    def test_transaction_generates_a_new_transaction_if_the_existing_transaction_does_not_match_price(self):
        self._mock_requests("<code>transaction321</code>", True)
        subscription = models.Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        profile = self.user.get_profile()
        transaction = models.Transaction.objects.create(
            subscription=subscription,
            price=models.PRICES[profile.type] * 2,
            code="abcd123",
            status="pending",
        )
        try:
            got_transaction = profile.transaction
            self.assertNotEqual(transaction.pk, got_transaction.pk)
            self.assertEqual(transaction.subscription, got_transaction.subscription)
            self.assertEqual(models.PRICES[profile.type], got_transaction.price)
            self.assertEqual("transaction321", got_transaction.code)
            transaction = models.Transaction.objects.get(pk=transaction.pk)
            self.assertEqual("canceled", transaction.status)
        finally:
            transaction.delete()
            subscription.delete()

    def test_transaction_generates_a_new_transaction_if_the_existing_transaction_is_canceled(self):
        self._mock_requests("<code>transaction123</code>", True)
        subscription = models.Subscription.objects.create(
            user=self.user,
            type="talk",
        )
        profile = self.user.get_profile()
        transaction = models.Transaction.objects.create(
            subscription=subscription,
            price=models.PRICES[profile.type],
            code="abcd123",
            status="canceled",
        )
        try:
            got_transaction = profile.transaction
            self.assertNotEqual(transaction.pk, got_transaction.pk)
            self.assertEqual(transaction.subscription, got_transaction.subscription)
            self.assertEqual(models.PRICES[profile.type], got_transaction.price)
            self.assertEqual("transaction123", got_transaction.code)
        finally:
            transaction.delete()
            subscription.delete()
