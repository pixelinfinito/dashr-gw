from __future__ import unicode_literals

import json

from mock import patch

from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from apps.core.models import Page
from apps.core.views import DepositSubmitApiView


class GetPageDetailsViewTest(TestCase):
    """ Tests for GetPageDetailsView view """

    def setUp(self):
        self.client = Client()
        self.page = Page.objects.create(title='test', slug='test')

    def test_getting_page_by_slug_valid(self):
        """ Test getting page by valid slug """

        response = self.client.get(
            reverse('page', kwargs={'slug': self.page.slug}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', content)
        self.assertIn('page', content)
        self.assertTrue(content['success'])
        self.assertEqual(content['page']['id'], self.page.pk)
        self.assertEqual(content['page']['slug'], self.page.slug)
        self.assertEqual(content['page']['title'], self.page.title)

    def test_getting_page_by_slug_invalid(self):
        """ Test getting page by invalid slug """

        response = self.client.get(
            reverse('page', kwargs={'slug': 'invalid'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', content)
        self.assertIn('page', content)
        self.assertIn('message', content)
        self.assertFalse(content['success'])
        self.assertEqual(content['message'], 'Page does not exists')
        self.assertEqual(len(content['page']), 0)

    def test_get_page_non_ajax(self):
        """ Test getting page by valid slug """

        response = self.client.get(
            reverse('page', kwargs={'slug': self.page.slug}), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')


class DepositSubmitApiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

    @patch('apps.core.models.DashWallet.get_new_address')
    def test_view_with_valid_form(self, patched_get_new_address):
        patched_get_new_address.return_value = ''
        request = self.factory.post(
            '',
            {'ripple_address': 'rp2PaYDxVwDvaZVLEQv7bHhoFQEyX1mEx7'},
        )
        response = DepositSubmitApiView.as_view()(request)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertIn('success', response_content)
        self.assertIn('dash_wallet', response_content)
        self.assertIn('status_url', response_content)
        self.assertEqual(response_content['success'], True)

    def test_view_with_invalid_form(self):
        request = self.factory.post('', {'ripple_address': 'Invalid address'})
        response = DepositSubmitApiView.as_view()(request)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertIn('success', response_content)
        self.assertIn('ripple_address_error', response_content)
        self.assertEqual(response_content['success'], False)
        self.assertEqual(
            response_content['ripple_address_error'],
            'The Ripple address is not valid.',
        )
