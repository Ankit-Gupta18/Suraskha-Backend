# smtp_client.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

class SMTPClient:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = os.getenv("SMTP_PORT", 587)
        self.sender_email = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "your-password")

    def send_verification_mail(self, recipient_email, subject, message, id_card_image):
        try:
            # Setup the MIME
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach the message body
            msg.attach(MIMEText(message, 'plain'))

            # Attach the ID card image
            if id_card_image:
                img = MIMEImage(id_card_image, name="id_card.png")
                msg.attach(img)

            # Create an SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable security
                server.login(self.sender_email, self.sender_password)  # Login with email and password
                server.send_message(msg)

            print(f"Verification email sent successfully to {recipient_email}")

        except Exception as e:
            print(f"Failed to send email: {e}")
            raise
