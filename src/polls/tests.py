import datetime

from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from model_mommy import mommy

from .models import Poll


class PollViewTests(TestCase):

    date_5_days_ago = timezone.now() + datetime.timedelta(days=-5)
    date_30_days_ago = timezone.now() + datetime.timedelta(days=-30)
    date_30_days_after = timezone.now() + datetime.timedelta(days=30)

    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    @patch('polls.tasks.send_email_about_new_poll.delay')
    def test_index_view_with_a_past_poll(self, mocked_task):
        mommy.make(Poll, question="Past poll.", pub_date=self.date_30_days_ago)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll.>'])

    @patch('polls.tasks.send_email_about_new_poll.delay')
    def test_index_view_with_a_future_poll(self, mocked_task):
        mommy.make(Poll, question="Future poll.", pub_date=self.date_30_days_after)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    @patch('polls.tasks.send_email_about_new_poll.delay')
    def test_index_view_with_future_poll_and_past_poll(self, mocked_task):
        mommy.make(Poll, question="Past poll.", pub_date=self.date_30_days_ago)
        mommy.make(Poll, question="Future poll.", pub_date=self.date_30_days_after)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll.>'])

    @patch('polls.tasks.send_email_about_new_poll.delay')
    def test_index_view_with_two_past_polls(self, mocked_task):
        mommy.make(Poll, question="Past poll 1", pub_date=self.date_30_days_ago)
        mommy.make(Poll, question="Past poll 2", pub_date=self.date_5_days_ago)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll 2>', '<Poll: Past poll 1>'])
