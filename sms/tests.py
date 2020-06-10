from django.test import TestCase
from .views import result
from .models import Contact
from unittest import mock


# Models Tests
class ContactTest(TestCase):

    def create_contact(self, firstname='John', lastname='Doe', email='jd@testmail.com', phonenumber='+15555555555', zipcode='55555', isPantry=False):
        return Contact.clients.create(firstname=firstname, lastname=lastname, email=email, phonenumber=phonenumber, zipcode=zipcode, isPantry=isPantry)

    def test_contact_creation(self):
        c = self.create_contact()
        self.assertTrue(isinstance(c, Contact))
        self.assertEqual(c.__str__(), 'John Doe')