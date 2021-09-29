from signalwire.rest import Client 

class SignalWire:
	def __init__(self, project_id, auth_token, space_url):
		self.project_id = project_id
		self.auth_token = auth_token
		self.space_url = space_url
		self.client = self.connect(project_id, auth_token, space_url)

	def connect(self, project_id, auth_token, space_url):
		self.client = Client(project_id, auth_token, signalwire_space_url=space_url)
		return self.client

	def send_sms(self, message, sender, recipient):
		message = self.client.messages.create(from_=sender, to=recipient, body=message)
		return message

import os
import argparse

if __name__ == "__main__":
	SIGNALWIRE_PROJECT_ID = os.getenv("SIGNALWIRE_PROJECT_ID")
	SIGNALWIRE_AUTH_TOKEN = os.getenv("SIGNALWIRE_AUTH_TOKEN") 
	SIGNALWIRE_SPACE_URL = os.getenv("SIGNALWIRE_SPACE_URL")
	SIGNALWIRE_NUMBER = os.getenv("SIGNALWIRE_NUMBER")

	parser = argparse.ArgumentParser(description="Send an SMS using Signalwire")
	parser.add_argument("message", help="the body of the SMS message", required=True)
	parser.add_argument("-s", "--sender", help=f"Your signalwire phone number ({SIGNALWIRE_NUMBER})", default=SIGNALWIRE_NUMBER, required=True)
	parser.add_argument("-r", "--recipient", help="The phone number to send SMS", required=True)
	args = parser.parse_args()
	print(args)

	if SIGNALWIRE_NUMBER and not sender:
		sender = SIGNALWIRE_NUMBER

	message = args.message
	sender = args.sender
	recipient = args.recipient
  
	client = SignalWire(SIGNALWIRE_PROJECT_ID, SIGNALWIRE_AUTH_TOKEN, SIGNALWIRE_SPACE_URL)
	print(f"message: {message}")
	print(f"sender: {sender}")
	print(f"recipient: {recipient}")
	print(f"client: {client}")

	print("not sending yet...still testing")