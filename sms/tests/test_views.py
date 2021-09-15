from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from sms.models import Contact
from sms.views import index,  sign_up, compose, result, upload

class ViewTestIndex(TestCase):
    '''
    every view needs access to the request factory
    '''
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
    
    def test_sms_index_view(self):
        url = reverse('index')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

class ViewTestCompose(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_sms_compose_view(self):
        url = reverse('compose')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)


class ViewTestUpload(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_sms_compose_view(self):
        url = reverse('upload')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

class ViewTestResult(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_sms_compose_view(self):
        url = reverse('result')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

class ViewTestSignup(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_sms_compose_view(self):
        url = reverse('sign-up')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)


