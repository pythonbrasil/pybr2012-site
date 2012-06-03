# -*- coding: utf-8 -*-
from django.core import management
from django.template import Context, Template
from django.test import TestCase, RequestFactory, Client
from django.views.generic import TemplateView, list as lview

from mittun.sponsors import models

import views


class MenuTemplateTagTestCase(TestCase):

    def test_should_make_a_menu_link_as_active(self):
        html = "{% load menu %}{% is_active request.get_full_path 'home' %}"
        template = Template(html)
        context = Context({'request': {"get_full_path": "/"}})

        self.assertEqual("active", template.render(context))

    def should_make_a_menu_link_as_not_active(self):
        html = "{% is_active request.get_full_path 'home' %}"
        template = Template(html)
        context = Context({'request': {"get_full_path": "register"}})

        self.assertNotEqual("active", template.render(context))


class AboutViewTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(views.AboutView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('about.html', views.AboutView.template_name)


class VenueViewTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(views.VenueView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('venue.html', views.VenueView.template_name)


class SponsorsInfoViewTestCase(TestCase):

    def test_should_be_a_template_view(self):
        self.assertTrue(issubclass(views.SponsorsInfoView, TemplateView))

    def test_shoud_use_a_venue_template(self):
        self.assertEqual('sponsors_info.html', views.SponsorsInfoView.template_name)


class CustomSponsorsViewTestCase(TestCase):
    fixtures = ['sponsors.json']

    def setUp(self):
        self.base_url = "http://localhost:8888"
        request = RequestFactory().get('sponsors')
        self.response = views.CustomSponsorsView.as_view()(request)

    def test_should_use_sponsors_template(self):
        self.assertIn('sponsors.html', self.response.template_name)

    def test_should_request_the_sponsors_url_and_be_success(self):
        response = Client().get('%s/sponsors/' % self.base_url)
        self.assertEqual(200, response.status_code)

    def test_should_have_sponsors_category_on_the_context(self):
        self.assertIn('sponsors_categories', self.response.context_data.keys())

    def test_should_order_the_sponsors_correctly(self):
        sponsor_categories = self.response.context_data['sponsors_categories']

        self.assertEqual(3, len(sponsor_categories))
        sponsor_1_category = sponsor_categories[0].name_en_us
        sponsor_2_category = sponsor_categories[1].name_en_us
        sponsor_3_category = sponsor_categories[2].name_en_us

        self.assertEqual("Diamond", sponsor_1_category)
        self.assertEqual("Gold", sponsor_2_category)
        self.assertEqual("FOSS", sponsor_3_category)


class SuccessfulPreRegistrationTestCase(TestCase):

    def test_should_be_a_template_view(self):
        assert issubclass(views.SuccessfulPreRegistration, TemplateView), "SuccessfulPreRegistration should be a TemplateView"

    def test_should_render_success_pre_registration_template(self):
        self.assertEqual("success_pre_registration.html", views.SuccessfulPreRegistration.template_name)


class HomeViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "sponsors.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_should_group_sponsor_into_groups_of_six(self):
        groups = views.Home().sponsor_groups()
        self.assertEqual(2, len(groups))
        self.assertEqual(6, len(groups[0]))

    def test_should_inherit_from_ListView(self):
        assert issubclass(views.Home, lview.ListView), "Home should inherit from ListView"

    def test_should_use_Sponsor_as_model(self):
        self.assertEqual(models.Sponsor, views.Home.model)

    def test_should_use_home_html_as_template(self):
        self.assertEqual("home.html", views.Home.template_name)

    def test_get_context_data_should_include_all_sponsor_groups_in_the_context(self):
        view = views.Home()
        context = view.get_context_data(object_list=[])
        sponsors = list(context["sponsor_groups"])
        self.assertEqual(view.sponsor_groups(), sponsors)


class InternationalizationWorkingFormAcceptLanguageTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8888"
        management.call_command("loaddata", "sponsors.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_should_return_portuguese_version_of_sponsor_category_name(self):
        response = Client().get('%s/sponsors/' % self.base_url, HTTP_ACCEPT_LANGUAGE='pt-br')
        self.assertEqual(200, response.status_code)
        self.assertIn('Diamante', response.content)

    def test_should_return_english_version_of_sponsor_category_name(self):
        response = Client().get('%s/sponsors/' % self.base_url, HTTP_ACCEPT_LANGUAGE='en-us')
        self.assertEqual(200, response.status_code)
        self.assertIn('Diamond', response.content)


class SporsorsJobViewTestCase(TestCase):

    def setUp(self):
        self.sponsors_jobs_view = views.SponsorsJobsView()

    def test_url_should_be_accessable(self):
        response = Client().get('/sponsors/jobs/')
        self.assertEqual(200, response.status_code)

    def test_template_name_should_be_sporsors_jobs(self):
        self.assertEqual("sponsors_jobs.html", self.sponsors_jobs_view.template_name)

    def test_model_should_be_jobs(self):
        self.assertEqual(models.Job, self.sponsors_jobs_view.model)

    def test_context_object_name_should_be_jobs(self):
        self.assertEqual("jobs", self.sponsors_jobs_view.context_object_name)
