# coding: utf-8

import unittest
from django.core import management
from django.core.urlresolvers import reverse
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
        url = reverse('proposal-page', kwargs={'proposal_id': 42,
                                               'proposal_slug': ''})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_incomplete_url_should_redirect_to_url_with_slug(self):
        url = reverse('proposal-page', kwargs={'proposal_id': 1,
                                               'proposal_slug': ''})
        response = self.client.get(url)
        expected_location = 'http://testserver/schedule/proposal/1/how-to-learn-python'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_location, response['Location'])

    def test_complete_url_should_return_200(self):
        url = reverse('proposal-page', kwargs={'proposal_id': 1,
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_should_have_proposal_information(self):
        url = reverse('proposal-page', kwargs={'proposal_id': 1,
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        self.assertEqual(response.context['proposal'],
                          Session.objects.get(pk=1))

    def test_should_have_speaker_info(self):
        url = reverse('proposal-page', kwargs={'proposal_id': 1,
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        speaker = AccountProfile.objects.get(user=User.objects.get(pk=1))
        self.assertEqual(len(response.context['speakers']), 1)
        speaker_response = response.context['speakers'][0]
        self.assertEqual(speaker_response['name'], speaker.name)
        self.assertEqual(speaker_response['twitter'], speaker.twitter)
        self.assertEqual(speaker_response['institution'], speaker.institution)
        self.assertEqual(speaker_response['bio'], speaker.description)
        self.assertEqual(speaker_response['profession'], speaker.profession)

    def test_should_include_speaker_without_profile(self):
        url = reverse('proposal-page', kwargs={'proposal_id': 2,
                'proposal_slug': 'how-to-learn-django'})
        response = self.client.get(url)
        speaker = user=User.objects.get(pk=2)
        self.assertEqual(len(response.context['speakers']), 2)
        speaker_response = response.context['speakers'][1]
        self.assertEqual(speaker_response['name'], speaker.username)
        self.assertEqual(speaker_response['twitter'], '')
        self.assertEqual(speaker_response['institution'], '')
        self.assertEqual(speaker_response['bio'], '')
        self.assertEqual(speaker_response['profession'], '')
