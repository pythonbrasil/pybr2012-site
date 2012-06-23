# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail as django_mail, management
from django.template import Context, Template
from django.test import TestCase, RequestFactory, Client
from django.views.generic import TemplateView, list as lview
from mittun.sponsors import models

from pythonbrasil8.core import mail, middleware, views
from pythonbrasil8.core.tests import mocks


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


class MailSenderTestCase(TestCase):

    def test_shoul_send_mail(self):
        m = mail.send(u"me@pythonbrasil.org.br", [u"he@pythonbrasil.org.br"], u"Hi", u"hello")
        m.wait()
        email = django_mail.outbox[0]
        self.assertEqual(u"Hi", email.subject)
        self.assertEqual(u"hello", email.body)
        self.assertEqual([u"he@pythonbrasil.org.br"], email.to)
        self.assertEqual(u"me@pythonbrasil.org.br", email.from_email)


class CacheMiddlewareTestCase(TestCase):

    def test_should_add_max_age_directive_to_the_value_in_settings(self):
        request = RequestFactory().get("/")
        request.user = User()
        request.user.is_authenticated = lambda: False
        m = mocks.ResponseMock()
        response = middleware.CacheMiddleware().process_response(request, m)
        self.assertEqual("max-age=%s" % settings.PAGE_CACHE_MAXAGE, response["Cache-Control"])

    def test_should_not_touch_the_value_of_Cache_control_if_it_is_defined(self):
        request = RequestFactory().get("/")
        request.user = User()
        request.user.is_authenticated = lambda: False
        m = mocks.ResponseMock()
        m["Cache-Control"] = "no-cache"
        response = middleware.CacheMiddleware().process_response(request, m)
        self.assertEqual("no-cache", response["Cache-Control"])

    def test_should_define_Cache_control_as_no_cache_if_the_user_is_authenticated(self):
        request = RequestFactory().get("/")
        request.user = User()
        request.user.is_authenticated = lambda: True
        m = mocks.ResponseMock()
        response = middleware.CacheMiddleware().process_response(request, m)
        self.assertEqual("no-cache", response["Cache-Control"])

    def test_should_remove_Vary_cookie_if_present(self):
        request = RequestFactory().get("/")
        request.user = User()
        request.user.is_authenticated = lambda: False
        m = mocks.ResponseMock()
        m["Vary"] = "Accept-Language, Cookie"
        response = middleware.CacheMiddleware().process_response(request, m)
        self.assertEqual("Accept-Language", response["Vary"])

    def test_should_be_the_first_in_middleware_list(self):
        self.assertEqual("pythonbrasil8.core.middleware.CacheMiddleware", settings.MIDDLEWARE_CLASSES[0])

    def test_should_not_cache_if_the_response_is_a_redirect(self):
        request = RequestFactory().get("/")
        m = mocks.ResponseMock()
        m.status_code = 301
        response = middleware.CacheMiddleware().process_response(request, m)
        self.assertEqual("no-cache", response["Cache-Control"])
