import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    """NotificationManager class uses Twilio's SMS & Whatsapp messaging services to send alerts"""
    def __init__(self):
        self.twilio_virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number = os.environ["TWILIO_VERIFIED_NUMBER"]
        self.twilio_whatsapp_number = os.environ["TWILIO_WHATSAPP_NUMBER"]
        self.email = os.environ['MY_EMAIL']
        self.email_password = os.environ['MY_EMAIL_PASSWORD']

        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        self.connection = smtplib.SMTP(os.environ['EMAIL_PROVIDER_SMTP_ADDRESS'])


    def send_sms(self, message_body):
        """This function takes message_body as a parameters to send message via SMS"""
        message = self.client.messages.create(
            body= message_body,
            from_=self.twilio_virtual_number,
            to=self.twilio_verified_number
        )

    def send_whatsapp(self, message_body):
        """This function takes message_body as a parameters to send message via Whatsapp"""
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp:{self.twilio_whatsapp_number}",
            to=f"whatsapp:{self.twilio_verified_number}"
        )

    def send_email(self, email_list, message_body):
        """This function takes email_list and message_body as a parameter to send emails via SMTP protocol"""
        with self.connection:
            self.connection.starttls()
            self.connection.login(user=self.email, password=self.email_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject: Start Planning a Trip 🛫 \n\n{message_body}".encode('utf-8')
                )
