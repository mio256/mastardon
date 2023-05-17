from django.test import TestCase
from django.urls import reverse


class PingViewTest(TestCase):
    def test_ping_view(self):
        response = self.client.get(reverse('ping_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"result": true}')


class IndexViewTest(TestCase):
    def test_index_view_no_query_params(self):
        response = self.client.get(reverse('index_view'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_query_params(self):
        response = self.client.get(reverse('index_view'), {'hours': '2', 'mode': 'sort', 'reb': '1', 'fav': '2', 'high': '50'})
        self.assertEqual(response.status_code, 200)
