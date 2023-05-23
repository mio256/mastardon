import datetime
from mastodon import utility
from django.test import TestCase
from django.urls import reverse
from . import chatgpt_func, mastodon_func

RESPONSE_LENGTH = 20
TIMELINE_PAGE = 3
TIMELINE_HOURS = 3


class PingViewTest(TestCase):
    def test_ping_view_response(self):
        response = self.client.get(reverse('ping_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"result": true}')


class IndexViewTest(TestCase):
    def test_index_view_response_without_query_params(self):
        response = self.client.get(reverse('index_view'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_response_with_query_params(self):
        response = self.client.get(reverse('index_view'), {'hours': '2', 'mode': 'sort', 'reb': '1', 'fav': '2', 'high': '50'})
        self.assertEqual(response.status_code, 200)


class MastodonFuncTest(TestCase):
    def setUp(self):
        self.response = mastodon_func.fetch_timeline()
        self.me = mastodon_func.fetch_me()

    def test_fetch_me(self):
        self.assertIsInstance(self.me, utility.AttribAccessList)
        self.assertIsInstance(self.me.id, str)

    def test_fetch_timeline_response(self):
        self.assertIsInstance(self.response, utility.AttribAccessList)
        self.assertEqual(len(self.response), RESPONSE_LENGTH)

    def test_timelines_page_response(self):
        response = mastodon_func.timelines_page(TIMELINE_PAGE)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), RESPONSE_LENGTH * TIMELINE_PAGE)

    def test_timeline_hours_response(self):
        response = mastodon_func.timelines_hours(TIMELINE_HOURS)
        self.assertIsInstance(response, list)
        d = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=TIMELINE_HOURS)
        self.assertLessEqual(response[-1].created_at, d)

    def test_timeline_last_response(self):
        response = mastodon_func.timelines_last(self.me.id)
        self.assertIsInstance(response, list)


class ChatGPTFuncTest(TestCase):
    def test_request_chatgpt_response(self):
        response = chatgpt_func.request_chatgpt(messages=[{"role": "user", "content": "hello"},])
        self.assertEqual(response["choices"][0]["message"]["role"], "assistant")
        self.assertIsInstance(response["choices"][0]["message"]["content"], str)

    def test_analyze_toots_response(self):
        mastodon_timelines = mastodon_func.fetch_timeline()
        id_list, gpt_response = chatgpt_func.analyze_toots(mastodon_timelines)
        self.assertIsInstance(id_list, list)
        self.assertIsInstance(gpt_response, str)
