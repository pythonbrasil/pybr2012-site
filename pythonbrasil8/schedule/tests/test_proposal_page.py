# coding: utf-8

from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from pythonbrasil8.schedule.models import Track, Session
from pythonbrasil8.dashboard.models import AccountProfile


class ProposalPageTestCase(TestCase):
    fixtures = ['sessions.json']

    def test_valid_track_but_inexistent_proposal_should_return_404(self):
        url = reverse('proposal-page', kwargs={'track_slug': 'newbiews',
                'proposal_slug': 'do-not-exist'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_correct_proposal_page_should_return_200(self):
        url = reverse('proposal-page', kwargs={'track_slug': 'newbies',
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_proposal_page_should_have_proposal_information(self):
        url = reverse('proposal-page', kwargs={'track_slug': 'newbies',
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        self.assertEqual(response.context['proposal'],
                          Session.objects.get(pk=1))

    def test_proposal_page_should_have_status_of_proposal(self):
        url = reverse('proposal-page', kwargs={'track_slug': 'newbies',
                'proposal_slug': 'how-to-learn-python'})
        response = self.client.get(url)
        self.assertIn(u'Accepted', response.content.decode('utf-8'))

        url = reverse('proposal-page', kwargs={'track_slug': 'newbies',
                'proposal_slug': 'how-to-learn-django'})
        response = self.client.get(url)
        self.assertIn(u'Not accepted', response.content.decode('utf-8'))

        url = reverse('proposal-page', kwargs={'track_slug':
            'just-another-track',
                'proposal_slug': 'i-dont-know-6'})
        response = self.client.get(url)
        self.assertIn(u'Confirmed', response.content.decode('utf-8'))

    def test_proposal_page_should_have_speaker_info(self):
        url = reverse('proposal-page', kwargs={'track_slug': 'newbies',
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

    def test_proposal_page_should_include_speaker_without_profile(self):
        url = reverse('proposal-page',
                kwargs={'track_slug': 'just-another-track',
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
