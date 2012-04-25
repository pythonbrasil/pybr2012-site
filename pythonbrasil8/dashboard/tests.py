from django.test import TestCase
from django.views.generic import TemplateView

from views import IndexView


class DashboardIndexTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(IndexView, TemplateView))

    def test_shoud_use_a_dashboard_template(self):
        self.assertEqual('dashboard/index.html', IndexView.template_name)
