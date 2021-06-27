import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharefest.settings")
import django
django.setup()
##necessary unittest code
import logging
from django.conf import settings
from django.test import TestCase
from .views import result, compose
from .models import Contact
from .view_helpers.messaging import send_multiple_sms
from unittest import mock
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

##########################
#### BEGIN MODEL TESTS ####
##########################

'''
assert that the contact model actually creates a contact
'''
class ContactTest(TestCase):

    def create_contact(self, firstname='John', 
    lastname='Doe', email='jd@testmail.com', 
    phonenumber='+15555555555', zipcode='55555', isPantry=False):
        return Contact.clients.create(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, zipcode=zipcode, isPantry=isPantry)

    def test_contact_creation(self):
        c = self.create_contact()
        self.assertTrue(isinstance(c, Contact))
        self.assertEqual(c.__str__(), 'John Doe')

##########################
#### BEGIN VIEW TESTS ####
##########################

# Test Sending SMS messages through muli-sms function



# @mock.patch('messaging.client.messages.create')
# def test_multiple_sms():
#     message_to_broadcast = 'example food pantry text'
#     expected_sid = 
    
    
    
    
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
