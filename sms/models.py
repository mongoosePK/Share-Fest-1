from django.db import models
from django.contrib.auth.models import *
from django.conf import settings
from phone_field import PhoneField
# Create contact model here.


class Contact(models.Model):
    '''
    
    '''
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    email = models.EmailField(blank=True)
    phonenumber = PhoneField(blank=True, help_text='Contact phone number')
    zipcode = models.CharField(max_length = 5)
    isPantry = models.BooleanField(null=True)
    clients = models.Manager()

    def __str__(self):
        return (f'{self.firstname} {self.lastname}')
    