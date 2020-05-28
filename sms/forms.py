from django import forms
import requests, json
from django.forms import ModelForm
from .models import Contact

class SMSForm(forms.Form):
    #here are the fields we'll be using to query the database 
    # for our contact model objects
    
    isPantry = forms.NullBooleanField(label='Send to Pantries', widget=forms.NullBooleanSelect)
    zip_code = forms.CharField(max_length=5, label='Zip', widget=forms.TextInput)
    body = forms.CharField(label='Message Body', widget=forms.Textarea)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('firstname','lastname','email','phonenumber','zipcode','isPantry')
