from django.test import TestCase
from django.template import Context, Template
from django.views.generic import TemplateView

from .views import VenueView


class TestMenuTemplateTag(TestCase):

    def should_make_a_menu_link_as_active(self):
        html = "{% is_active request.get_full_path 'home' %}"
        template = Template(html)
        context = Context({'request': {"get_full_path": "home"}})

        self.assertEqual("active", template.render(context))

    # def should_make_a_menu_link_as_not_active(self):
    #     html = "{% is_active request.get_full_path 'home' %}"
    #     template = Template(html)
    #     context = Context({'request': {"get_full_path": "register"}})

    #     self.assertNotEqual("", template.render(context))


class VenueViewTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(VenueView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('venue.html', VenueView.template_name)
