# -*- coding: utf-8 -*-
import unittest

from django.template import response
from django.test import client

from pythonbrasil8.schedule import views


class FinishedViewTestCase(unittest.TestCase):

    def test_template_name(self):
        self.assertEqual("schedule/finished_proposals.html",
                         views.FinishedProposalsView.template_name)

    def test_get(self):
        request = client.RequestFactory().get("/")
        resp = views.FinishedProposalsView().get(request)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual(views.FinishedProposalsView.template_name,
                         resp.template_name)
