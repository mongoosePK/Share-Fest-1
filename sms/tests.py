from django.conf import settings
from django.test import TestCase
from .views import result, compose
from .models import Contact
from unittest import mock
from twilio.rest import Client

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
      - test message sending function
      - test upload function

      NOTE: this test is based off of twilio's PYTEST testing
            documentation.
'''

# Test Sending SMS messages through Twilio client
# With Test Credentials
# messages: POST /2010-04-01/Accounts/{TestAccountSid}/Messages
def testSms():
    '''
    This function tests the twilio client SMS functionality using test tokens.
    the call returns a json response but I've only printed the message sid 
    to just verify that things didn't break
    read more about twilio testing here: 
    https://www.twilio.com/docs/iam/test-credentials#test-sms-messages
    '''
    client = Client(settings.TEST_ACCOUNT_SID, settings.TEST_AUTHTOKEN)
    message = client.messages.create(
        body='The Earth is Blue, how wonderful, it is amazing.',
        from_='+15005550006',
        to='+18034047382'
    )
    
    print(message.sid)
    
