# works with both python 2 and 3
from __future__ import print_function
import datetime 

import africastalking

class SMS:

	def __init__(self):

		# Set your app credentials
		self.username = "sandbox"
		self.api_key = "47246e11613b9f71c704e8d8dea56ae4f2c2fae8382152572fc8c56c6f8426f5"

		# Initialize the SDK
		africastalking.initialize(self.username, self.api_key)

		# Get the SMS service
		self.sms = africastalking.SMS

	def send(self):
			# Set the numbers you want to send to in international format
			recipients = ["+2547989847"]

			# Set your message
			message = "Hello, your results are ready. Kindly come and pick them within the next 7 working Days() \n @TeamBankai " ;

			# Set your shortCode or senderId
			sender = "72225"
			try:
				# Thats it, hit send and we'll take care of the rest.
				response = self.sms.send(message, recipients, sender)
				print (response)
			except Exception as e:
				print ('Encountered an error while sending: %s' % str(e))

if __name__ == '__main__':
	SMS().send()
	
	
