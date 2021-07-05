
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

# Models Tests
'''
TODO: assert that the contact model actually creates a contact
'''
class ContactTest(TestCase):

    def create_contact(self, firstname='John', lastname='Doe', email='jd@testmail.com', phonenumber='+15555555555', zipcode='55555', isPantry=False):
        return Contact.clients.create(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, zipcode=zipcode, isPantry=isPantry)

    def test_contact_creation(self):
        c = self.create_contact()
        self.assertTrue(isinstance(c, Contact))
        self.assertEqual(c.__str__(), 'John Doe')

'''
TODO: - Factor SMS sending cunction in compose() into its own function sendSMS(to, from, message)
      - put test credentials in to the .env file
      - test message sending function
      - test upload function

      NOTE: this test is based off of twilio's PYTEST testing
            documentation.
'''

# @mock.patch('messaging.client.messages.create')
# def test_multiple_sms():
#     message_to_broadcast = 'example food pantry text'
#     expected_sid = 
    
    
# test_twilio_api() validates the twilio account credentials
# by using test credentials which mimic actual funtionality without
# creating any sms traffic. 
    
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
