import datetime, os, logging
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import request, response
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharefest.settings")
import django
django.setup()

from django.conf import settings
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse

from .models import Contact
from .views import index, sign_up, compose, result, upload
from .view_helpers.messaging import send_multiple_sms
from .forms import SMSForm, ContactForm, UploadForm

from unittest import mock
from unittest.mock import MagicMock
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

##########################
#### BEGIN MODEL TESTS ####
##########################

'''
assert that the contact model actually creates a contact
'''
class ContactTest(TestCase):

    def create_contact(self, firstname='John', lastname='Doe', email='jd@testmail.com', 
    phonenumber='+15555555555', zipcode='55555', isPantry=False):
        return Contact.clients.create(firstname=firstname, lastname=lastname, 
        email=email, phonenumber=phonenumber, zipcode=zipcode, isPantry=isPantry)

    def test_contact_creation(self):
        c = self.create_contact()
        self.assertTrue(isinstance(c, Contact))
        self.assertEqual(c.__str__(), 'John Doe')

##########################
#### BEGIN VIEW TESTS ####
##########################
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


##########################
#### BEGIN FORM TESTS ####
##########################
class FormTest(TestCase):
    """
    TESTS: form.is_valid
    """
    def create_contact(self, firstname='tony', lastname='tester', email='test@tester.com', 
    phonenumber='+15555555555', zipcode='55555', isPantry=True):
        return Contact.clients.create(firstname=firstname, lastname=lastname, 
        email=email, phonenumber=phonenumber, zipcode=zipcode, isPantry=isPantry)
    
    def test_valid_SMSForm(self):
        data = {
            'isPantry': True, 'zip_code': '60504', 'body': 'test text'
        }
        form = SMSForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_SMSForm(self):
        data = {
            'isPantry': True, 'zip_code': '60504', 'body': ''
        }
        form = SMSForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_ContactForm(self):
        c = self.create_contact()
        data = {'firstname': c.firstname, 'lastname': c.lastname, 'email': c.email,
        'phonenumber': c.phonenumber, 'zipcode': c.zipcode, 'isPantry': c.isPantry,}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_ContactForm(self):
        c = self.create_contact()
        data = {'firstname': '', 'lastname': c.lastname, 'email': c.email,
        'phonenumber': c.phonenumber, 'zipcode': c.zipcode, 'isPantry': c.isPantry,}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())

##########################
#### BEGIN API TESTS #####
##########################
def test_twilio_api():
    client = Client(settings.TEST_ACCOUNT_SID, settings.TEST_AUTHTOKEN)
    try:
        message = client.messages.create(
            body='The Earth is Blue, how wonderful, it is amazing.',
            from_='+15005550006',
            to='+18034047382'
        )
    except TwilioRestException as e:
        logging.error(f'oh no: {e}')
    
    assert message.sid is not None

# test_send_multiple_sms() tests the functionality of the 
# mass SMS sending function, a list of valid 'magic' numbers
# using our test tokens. 

def test_send_multiple_sms():
    recipientPhoneNumbers = [+15005550010,+15005550011,+15005550012,+15005550013,
    +15005550014,+15005550015,+15005550016,+15005550017,+15005550018,+15005550019]
    client = Client(settings.TEST_ACCOUNT_SID, settings.TEST_AUTHTOKEN)
    failedNumbers = list()
    for recipient in recipientPhoneNumbers:
            if recipient:
                try:
                    message = client.messages.create(to=recipient,
                    from_='+15005550006',
                    body='Lots of imaginary texts just went out')
                except TwilioRestException as e:
                    print(e)
                    failedNumbers.append(str(recipient))
    assertCountEqual(message.to, recipientPhoneNumbers)
