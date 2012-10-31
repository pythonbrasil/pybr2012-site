# coding: utf-8

from django.core.urlresolvers import reverse
from django.test import TestCase
from pythonbrasil8.schedule.models import Track, Session


class ScheduleTestCase(TestCase):
    fixtures = ['sessions.json']

    def test_list_all_tracks(self):
        url = reverse('schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        for track in Track.objects.all():
            self.assertIn(track.name, content)
            self.assertIn(track.slug, content)

    def test_list_only_accepted_talks(self):
        url = reverse('schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        for session in Session.objects.filter(type='talk'):
            if session.status in ['accepted', 'confirmed']:
                self.assertIn(session.title, content)
            else:
                self.assertNotIn(session.title, content)
