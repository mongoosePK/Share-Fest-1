from django.test import TestCase
from .views import result, compose
from .models import Contact
from unittest import mock


# Models Tests
'''
TODO: assert that the contact model actually creates a contact
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

'''
TODO: - Factor SMS sending cunction in compose() into its own function sendSMS(to, from, message)
      - put test credentials in to the .env file
      - test message sending function
      - test upload function

      NOTE: this test is based off of twilio's PYTEST testing
            documentation.
'''

# def test_compose_sms():
#     message = "This is a test."
#     to = "+18034047382"
#     from_ = "+12017333892"
#     assert send_message(to, from_, message) is not None