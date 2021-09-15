import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharefest.settings")
from django.test import TestCase
from sms.models import Contact
from sms.forms import SMSForm, ContactForm, UploadForm


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
