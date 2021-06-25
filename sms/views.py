from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .forms import SMSForm, ContactForm, UploadForm
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
    return render(request, 'sign_up.html', {'form':form})


@login_required
def compose(request):
    '''
    the compose() view renders our messaging form
    ''' 

    form = SMSForm()
    context = {'form': form}

    return render(request, 'compose.html', context=context)

@login_required
def result(request):
    '''
    result() takes the form data from compose() and validates it.
    it creates a filtered list of clients with matching zipcodes 
    (or all clients if zip is 00000)

    it then invokes the messaging client from a helper function
    file, using the form data to create the message body.
    '''

    if request.method == 'GET':
        form = SMSForm(request.GET)

        if form.is_valid():
            is_pantry = form.cleaned_data.get('isPantry', '')
            zip_code = form.cleaned_data.get('zip_code', '')
            body = form.cleaned_data.get('body', '')
    

    ### GET ALL CLIENTS if ZIP is 0000 ####
    if zip_code == '00000':
        recipients = get_list_or_404(Contact.clients.all())
    # filter relevant clients
    else:
        recipients = get_list_or_404(Contact.clients.filter(zipcode = zip_code).
        filter(isPantry = is_pantry))

    # create list of recipient phone numbers
    recipientPhoneNumbers = list()
    failedNumbers = list()
    for recipient in recipients:
        recipientPhoneNumbers.append(str(recipient.phonenumber))
    # invoke twilio messaging client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message_to_broadcast = (f'{body}')
    
    # iteratively send mesages to clients in list    
    for recipient in recipientPhoneNumbers:
        if recipient:
            try:
                message = client.messages.create(to=recipient,messaging_service_sid=settings.MESSAGING_SERVICE_SID, body=message_to_broadcast)
            except TwilioRestException as e:
                print(e)
                failedNumbers.append(str(recipient))

    context = {
        'recipient' : recipients,
        'message_body' : message.body,
        'message_sid' : message.sid,
        'failed_numbers': failedNumbers
    }
    return render(request, 'result.html', context=context)

@login_required
def upload(request):
    '''
    upload() takes csv files of food pantry clients and creates Contacts from them.
    Currently, it decides how to order the columns based on the source of the .csv
    
    TODO: - better file validation 
          - file type error handling
    '''
    form = UploadForm()
    template = 'upload.html'

    if request.method == 'GET':
        return render(request, template, {'form': form})

    csv_file = request.FILES['inputFile']
    
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'this is not a csv file')
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    
    # skip first line because it is suposed to be a header
    # the uploadType should be standard for now, but different pantries
    # use different formats. Currently I import the client contact list
    # from a web service called Planning Center because it handles duplicate 
    # contacts and updates pretty well
    if request.POST['uploadType'] == 'P':
        next(io_string)
        for row in csv.reader(io_string, delimiter=',', quotechar='|'):
            if row[42]:
                _, created = Contact.clients.update_or_create(
                    firstname=row[3],
                    lastname=row[6],
                    email='',
                    phonenumber=row[42],
                    zipcode=row[31],
                    isPantry=False
                )

    context = {
        'form' : form
    }
    return render(request, template, {'form': form})
