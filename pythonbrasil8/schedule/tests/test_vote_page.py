# coding: utf-8

import unittest
import json
from django.core import management
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from pythonbrasil8.schedule.models import Track, Session, ProposalVote
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

class ProposalVoteTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        management.call_command("loaddata", "sessions.json", verbosity=0)

    def tearDown(self):
        management.call_command("flush", verbosity=0, interactive=False)

    def _login(self):
        self.client.user = User.objects.create_user(username='user',
                                                    password='test')
        self.client.login(username='user', password='test')

    def test_should_redirect_user_that_is_not_logged_in(self):
        url = reverse('proposal_vote', kwargs={'proposal_id': 1,
                                               'type_of_vote': 'up'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_should_only_allow_post_method(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'up'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_should_return_404_when_invalid_type_of_vote(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 1,
                                               'type_of_vote': 'python'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_should_return_404_when_invalid_proposal_id(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 9999999,
                                               'type_of_vote': 'up'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_should_return_404_if_trying_to_vote_for_a_tutorial(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 1,
                                               'type_of_vote': 'up'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_should_insert_one_row_if_vote_up(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'up'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        session = Session.objects.get(pk=3)
        votes = ProposalVote.objects.filter(session=session, vote=1,
                                            user=self.client.user)
        self.assertEqual(votes.count(), 1)

        url = reverse('proposal_vote', kwargs={'proposal_id': 4,
                                               'type_of_vote': 'down'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        session = Session.objects.get(pk=4)
        votes = ProposalVote.objects.filter(session=session, vote=-1,
                                            user=self.client.user)
        self.assertEqual(votes.count(), 1)

    def test_if_an_idiot_vote_more_than_once_for_the_same_talk_should_only_insert_one_row(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'up'})
        for i in range(5):
            self.client.post(url)
        session = Session.objects.get(pk=3)
        votes = ProposalVote.objects.filter(session=session, vote=1,
                                            user=self.client.user)
        self.assertEqual(votes.count(), 1)

        url = reverse('proposal_vote', kwargs={'proposal_id': 4,
                                               'type_of_vote': 'down'})
        for i in range(5):
            self.client.post(url)
        session = Session.objects.get(pk=4)
        votes = ProposalVote.objects.filter(session=session, vote=-1,
                                            user=self.client.user)
        self.assertEqual(votes.count(), 1)

    def test_neutral_votes_should_remove_record_for_that_user_and_talk(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'neutral'})
        self.client.post(url)
        session = Session.objects.get(pk=3)
        votes = ProposalVote.objects.filter(session=session,
                                            user=self.client.user)
        self.assertEqual(votes.count(), 0)

    def test_alternated_votes_should_record_only_the_last_one(self):
        self._login()
        types_of_vote = ('up', 'down', 'neutral')
        for type_1 in types_of_vote:
            for type_2 in types_of_vote:
                url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                                       'type_of_vote': type_1})
                self.client.post(url)
                url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                                       'type_of_vote': type_2})
                self.client.post(url)

                session = Session.objects.get(pk=3)
                votes = ProposalVote.objects.filter(session=session,
                                                    user=self.client.user)
                if type_2 == 'up':
                    self.assertEqual(votes.count(), 1)
                    self.assertEqual(votes[0].vote, 1)
                elif type_2 == 'down':
                    self.assertEqual(votes.count(), 1)
                    self.assertEqual(votes[0].vote, -1)
                if type_2 == 'neutral':
                    self.assertEqual(votes.count(), 0)

    def test_should_return_a_JSON_with_vote_information(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'neutral'})
        response = self.client.post(url)
        result = json.loads(response.content)
        self.assertEqual(result, {'proposal_id': 3, 'vote': 'neutral'})

        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'up'})
        response = self.client.post(url)
        result = json.loads(response.content)
        self.assertEqual(result, {'proposal_id': 3, 'vote': 'up'})

        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'down'})
        response = self.client.post(url)
        result = json.loads(response.content)
        self.assertEqual(result, {'proposal_id': 3, 'vote': 'down'})

    def test_should_load_past_votes(self):
        self._login()
        url = reverse('proposal_vote', kwargs={'proposal_id': 2,
                                               'type_of_vote': 'up'})
        self.client.post(url)

        url = reverse('proposal_vote', kwargs={'proposal_id': 3,
                                               'type_of_vote': 'neutral'})
        self.client.post(url)
        url = reverse('proposal_vote', kwargs={'proposal_id': 4,
                                               'type_of_vote': 'neutral'})
        self.client.post(url)


        url = reverse('proposal_vote', kwargs={'proposal_id': 6,
                                               'type_of_vote': 'down'})
        self.client.post(url)
        url = reverse('proposal_vote', kwargs={'proposal_id': 7,
                                               'type_of_vote': 'down'})
        self.client.post(url)
        url = reverse('proposal_vote', kwargs={'proposal_id': 8,
                                               'type_of_vote': 'down'})
        self.client.post(url)

        response = self.client.get(reverse('vote_page'))
        content = response.content.decode('utf-8')
        self.assertEqual(content.count('up_active.png'), 1)
        self.assertEqual(content.count('neutral_active.png'), 2)
        self.assertEqual(content.count('down_active.png'), 3)
