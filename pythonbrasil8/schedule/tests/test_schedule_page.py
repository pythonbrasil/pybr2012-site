# coding: utf-8

import unittest
from django.core import management
from django.core.urlresolvers import reverse
from django.test.client import Client
from pythonbrasil8.schedule.models import Track


class ScheduleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        management.call_command("loaddata", "sessions.json", verbosity=0)

    def tearDown(self):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_list_all_tracks(self):
        url = reverse('schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        return
        for track in Track.objects.all():
            self.assertIn(track.name, content)
            self.assertIn(track.slug, content)
