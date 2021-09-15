from django.test import TestCase, Client
from django.conf import settings
import logging
from twilio.base.exceptions import TwilioRestException
import unittest

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
