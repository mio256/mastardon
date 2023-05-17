from django.test import TestCase
from django.http import JsonResponse
from django.template.response import TemplateResponse


class PingTestCase(TestCase):
    def testResponseType(self):
        response = self.client.get('/ping/')
        self.assertEqual(type(response), JsonResponse)

    def testResponseContent(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.json(), {'result': True})


class IndexTestCase(TestCase):
    def testResponseType(self):
        response = self.client.get('/')
        self.assertEqual(type(response), TemplateResponse)

    def testResponseTypeSort(self):
        response = self.client.get('/?mode=sort')
        self.assertEqual(type(response), TemplateResponse)

    def testResponseTypeGPT(self):
        response = self.client.get('/?mode=gpt')
        self.assertEqual(type(response), TemplateResponse)
