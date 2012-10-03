# coding: utf-8

import unittest
from django.core import management
from django.test.client import Client
from django.contrib.auth.models import User
from pythonbrasil8.schedule.models import Session
from pythonbrasil8.dashboard.models import AccountProfile


class ProposalPageTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        management.call_command("loaddata", "sessions.json", verbosity=0)

    def tearDown(self):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_inexistent_proposal_should_return_404(self):
        response = self.client.get('/schedule/proposal/42/')
        self.assertEquals(response.status_code, 404)

    def test_incomplete_url_should_redirect_to_url_with_slug(self):
        response = self.client.get('/schedule/proposal/1/')
        self.assertEquals(response.status_code, 302)

    def test_complete_url_should_return_200(self):
        response = self.client.get('/schedule/proposal/1/how-to-learn-python')
        self.assertEquals(response.status_code, 200)

    def test_should_have_proposal_information(self):
        response = self.client.get('/schedule/proposal/1/how-to-learn-python')
        self.assertEquals(response.context['proposal'],
                          Session.objects.get(pk=1))

    def test_should_have_speaker_info(self):
        response = self.client.get('/schedule/proposal/1/how-to-learn-python')
        speaker = AccountProfile.objects.get(user=User.objects.get(pk=1))
        self.assertEquals(len(response.context['speakers']), 1)
        speaker_response = response.context['speakers'][0]
        self.assertEquals(speaker_response['name'], speaker.name)
        self.assertEquals(speaker_response['twitter'], speaker.twitter)
        self.assertEquals(speaker_response['institution'], speaker.institution)
        self.assertEquals(speaker_response['bio'], speaker.description)
        self.assertEquals(speaker_response['profession'], speaker.profession)

    def test_should_include_speaker_without_profile(self):
        response = self.client.get('/schedule/proposal/2/how-to-learn-django')
        speaker = user=User.objects.get(pk=2)
        self.assertEquals(len(response.context['speakers']), 2)
        speaker_response = response.context['speakers'][1]
        self.assertEquals(speaker_response['name'], speaker.username)
        self.assertEquals(speaker_response['twitter'], '')
        self.assertEquals(speaker_response['institution'], '')
        self.assertEquals(speaker_response['bio'], '')
        self.assertEquals(speaker_response['profession'], '')
