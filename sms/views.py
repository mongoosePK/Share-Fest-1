from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
from .forms import SMSForm, ContactForm, get_numbers, get_all_numbers
from .models import Contact
import datetime, csv, io

@login_required
def index(request):
    today = datetime.datetime.now().date()
    return render(request, 'index.html', {'today':today})

@login_required
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #log user in
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html',{'form':form})

@login_required
def compose(request):
    form = SMSForm()
    context = {'form': form}


    return render(request, 'compose.html', context=context)

@login_required
def result(request):
    if request.method == 'GET':
        form = SMSForm(request.GET)

        if form.is_valid():
            is_pantry = form.cleaned_data.get('isPantry', '')
            zip_code = form.cleaned_data.get('zip_code', '')
            body = form.cleaned_data.get('body', '')
    
    # after we validate the form data we pass the
    recipients = get_list_or_404(Contact.clients.filter(zipcode = zip_code).filter(isPantry = is_pantry))
    recipientPhoneNumbers = list()
    for recipient in recipients:
        recipientPhoneNumbers.append(str(recipient.phonenumber))
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message_to_broadcast = (f'{body}')
    for recipient in recipientPhoneNumbers:
        if recipient:
            message = client.messages.create(to=recipient,messaging_service_sid=settings.MESSAGING_SERVICE_SID,
            body=message_to_broadcast)

    context = {
        'recipient' : recipients,
        'message_body' : message.body,
        'message_sid' : message.sid
    }
    return render(request, 'result.html', context=context)

@login_required
def upload(request):
    template = 'upload.html'
    prompt = {
        'order' : 'Order of the CSV should be first_name, last name,  email, phone number, zip, isPantry.'
    }
    if request.method == 'GET':
        return render(request, template)
    csv_file = request.FILES['file']
    
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'this is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    #skip first line because it is suposed to be a header
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Contact.clients.update_or_create(
            firstname=column[0],
            lastname=column[1],
            email=column[2],
            phonenumber=column[3],
            zipcode=column[4],
            isPantry=column[5]
        )
    context = {}
    return render(request, template, context)
