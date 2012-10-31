# coding: utf-8

from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
from pythonbrasil8.schedule.models import Session


class NewTrackPage(TestCase):
    fixtures = ['sessions.json']

    def test_track_page_should_redirect_to_schedule_page(self):
        url = reverse('track-page', kwargs={'track_slug': 'newbies'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        next_url = response.get('location', None)
        self.assertEqual(next_url, 'http://testserver' + reverse('schedule'))

        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        next_url = response.get('location', None)
        self.assertEqual(next_url, 'http://testserver' + reverse('schedule'))

@skip('Track should redirect to accepted proposals')
class TrackPageTestCase(TestCase):
    fixtures = ['sessions.json']

    def test_inexistent_track_should_return_404(self):
        url = reverse('track-page', kwargs={'track_slug': 'do-not-exist'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_track_page_should_list_all_proposals_to_that_track(self):
        url = reverse('track-page', kwargs={'track_slug': 'newbies'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        for proposal in Session.objects.filter(track=1):
            self.assertIn(proposal.title, content)
            self.assertIn(proposal.slug, content)
