# -*- coding: utf-8 -*-
from django.core import management
from django.test import TestCase
from django.template import Context, Template
from django.views.generic import TemplateView
from django.views.generic import list as lview

from mittun.sponsors import models

from core import views


class MenuTemplateTagTestCase(TestCase):

    def test_should_make_a_menu_link_as_active(self):
        html = "{% load menu %}{% is_active request.get_full_path 'home' %}"
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
        self.assertTrue(issubclass(views.VenueView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('venue.html', views.VenueView.template_name)


class SponsorViewTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(views.SponsorView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('sponsor.html', views.SponsorView.template_name)

class SuccessfulPreRegistrationTestCase(TestCase):

    def test_should_be_a_template_view(self):
        assert issubclass(views.SuccessfulPreRegistration, TemplateView), "SuccessfulPreRegistration should be a TemplateView"

    def test_should_render_success_pre_registration_template(self):
        self.assertEqual("success_pre_registration.html", views.SuccessfulPreRegistration.template_name)


class HomeViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "sponsors.json", verbosity=0)

        cls.sponsors = list(models.Sponsor.objects.all())

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_should_inherit_from_ListView(self):
        assert issubclass(views.Home, lview.ListView), "Home should inherit from ListView"

    def test_should_use_Sponsor_as_model(self):
        self.assertEqual(models.Sponsor, views.Home.model)

    def test_should_use_home_html_as_template(self):
        self.assertEqual("home.html", views.Home.template_name)

    def test_get_context_data_should_include_all_sponsors_in_the_context(self):
        view = views.Home()
        context = view.get_context_data(object_list=[])
        sponsors = list(context["sponsors"])
        self.assertEqual(sponsors, self.sponsors)
