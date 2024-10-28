import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import EmailSettings


def send_password_email(password : str, receiver_email : str):
    email_settings = EmailSettings()

    message = MIMEMultipart("alternative")
    message["Subject"] = "EuroDental Account Password"
    message["From"] = email_settings.email
    message["To"] = receiver_email

    html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #0073e6; text-align: center;">Welcome to EuroDental!</h2>
                <p>Dear User,</p>
                <p>Here is your temporary password to log in to your EuroDental account:</p>
                <p style="font-size: 18px; font-weight: bold; color: #333;">{password}</p>
                <p>To access your account and get started, please click the link below:</p>
                <p style="text-align: center; margin: 20px 0;">
                    <a href="http://35.180.66.24/login" style="display: inline-block; padding: 10px 20px; background-color: #0073e6; color: white; text-decoration: none; border-radius: 5px;">Log in to your account</a>
                </p>
                <p>If you didn't request this email, please ignore it.</p>
                <p>Best regards,<br>EuroDental Support Team</p>
            </div>
        </body>
        </html>
        """

    # Combine headers and body content correctly
    text = f"Subject: Welcome to EuroDental!\n\n Here is your temporary password to log in to your EuroDental account: {password}"

    html_part = MIMEText(html,"html")
    text_part = MIMEText(text,"plain")

    message.attach(text_part)
    message.attach(html_part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(email_settings.smtp_server,email_settings.e_port,context=context) as server:
        server.login(email_settings.email,email_settings.e_password)
        server.sendmail(email_settings.email,receiver_email,message.as_string())
