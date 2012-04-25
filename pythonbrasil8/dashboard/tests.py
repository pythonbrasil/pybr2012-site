from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from views import IndexView


class DashboardIndexTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(IndexView, TemplateView))

    def test_shoud_use_a_dashboard_template(self):
        self.assertEqual('dashboard/index.html', IndexView.template_name)

    def test_should_redirects_if_user_is_not_logged_in(self):
        request = RequestFactory().get("/")
        user = User()
        user.is_authenticated = lambda : False
        request.user = user
        result = IndexView.as_view()(request)
        self.assertEqual(302, result.status_code)

    def test_should_have_200_status_code_when_user_is_logged_in(self):
        request = RequestFactory().get("/")
        request.user = User()
        result = IndexView.as_view()(request)
        self.assertEqual(200, result.status_code)
