from django import forms
import requests, json
from django.forms import ModelForm
from .models import Contact

UPLOAD_TYPE = [('N', 'Null'),('P', 'Planning Center')]


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

class UploadForm(forms.Form):
    
    uploadType = forms.ChoiceField(label='Upload Type', widget=forms.RadioSelect, choices=UPLOAD_TYPE)
    inputFile = forms.FileField(label='Input File')
