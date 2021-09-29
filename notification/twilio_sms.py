import os
from time import sleep
from twilio.rest import Client as Twilio

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

RECIPIENT_NUMBER = os.getenv("SMS_RECIPIENT_NUMBER")

twilio = Twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = {
    "body" : "test SMS from Twilio",
    "from_" : TWILIO_NUMBER,
    "to" : RECIPIENT_NUMBER 
}

response = twilio.messages.create(**message)

while response.status not in ["delivered", "failed"]:
    print(F"waiting for SMS status: {response.status}")
    sleep(3)
    response = response.fetch()

if response.status == "failed":
    raise Exception("failed to send SMS")
elif response.status == "delivered": 
    print("delivered")
else:
    print("what?")


print(response)
print(response.sid)
print(response.account_sid)
print(response.body)
print(response.error_message, response.error_code)
print(response.status) # sending, sent, queued, delivered, failed, etc
