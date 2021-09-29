import smtplib

carriers = {
	'att':'mms.att.net',
	'verizon':'vtext.com',
	'tmobile':'tmomail.net',
	'sprint':'page.nextel.com'
}

def send_sms(message, number, carrier, email_address, email_password):
	sms_address = f"{number}@{carriers[carrier]}"
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email_address, email_password)
	server.sendmail(email_address, sms_address, message)
	server.quit()
	