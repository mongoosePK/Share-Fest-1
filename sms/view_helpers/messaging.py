from twilio.base.exceptions import TwilioRestException
from django.conf import settings

def send_multiple_sms(recipientPhoneNumbers, client, message_to_broadcast):
    failedNumbers = list()
    for recipient in recipientPhoneNumbers:
            if recipient:
                try:
                    message = client.messages.create(to=recipient,
                    messaging_service_sid=settings.MESSAGING_SERVICE_SID,
                    body=message_to_broadcast)
                except TwilioRestException as e:
                    print(e)
                    failedNumbers.append(str(recipient))
    return (message.sid, failedNumbers)
