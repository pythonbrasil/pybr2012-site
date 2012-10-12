# coding: utf-8

import unittest
from django.core import management
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from pythonbrasil8.schedule.models import Track, Session
from pythonbrasil8.dashboard.models import AccountProfile


class VotePageTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        management.call_command("loaddata", "sessions.json", verbosity=0)

    def tearDown(self):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_vote_page_should_redirect_user_that_is_not_logged_in(self):
        url = reverse('vote_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_vote_page_should_return_200_for_user_that_is_logged_in(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_tracks_should_appear_on_vote_page(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')
        response = self.client.get(url)
        content = response.content.decode('utf8')
        tracks = Track.objects.all()
        for track in tracks:
            self.assertIn(track.name, content)

    def test_all_sessions_should_appear_on_each_track(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')
        response = self.client.get(url)
        content = response.content.decode('utf8')
        sessions = Session.objects.filter(type='talk')
        for session in sessions:
            self.assertIn(session.title, content)

    def test_tracks_should_appear_in_random_order(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')

        tracks = []
        for i in range(50):
            response = self.client.get(url)
            tracks_and_sessions = response.context['tracks_and_sessions']
            tracks.append([track for track, sessions in tracks_and_sessions])

        diff_counter = 0
        for track in tracks[1:]:
            self.assertEqual(set(track), set(tracks[0]))
            if tracks[0] != track:
                diff_counter += 1

        self.assertTrue(diff_counter > 0)

    def test_only_talk_proposals_should_appear(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')

        response = self.client.get(url)
        tracks_and_sessions = dict(response.context['tracks_and_sessions'])
        proposals = set()
        for tracks, sessions in tracks_and_sessions.items():
            proposals.update(sessions)
        talk_proposals = set(list(Session.objects.filter(type='talk')))
        self.assertEqual(talk_proposals, proposals)

    def test_sessions_should_appear_in_random_order_inside_a_track(self):
        url = reverse('vote_page')
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')

        tracks_and_sessions = []
        for i in range(50):
            response = self.client.get(url)
            these_tracks = dict(response.context['tracks_and_sessions'])
            tracks_and_sessions.append(these_tracks)
        tracks = Track.objects.all()
        for track in tracks:
            diff_counter = 0
            first_request = tracks_and_sessions[0][track]
            for ts in tracks_and_sessions[1:]:
                self.assertEqual(set(ts[track]), set(first_request))
                if ts[track] != first_request:
                    diff_counter += 1
            self.assertTrue(diff_counter > 0)
