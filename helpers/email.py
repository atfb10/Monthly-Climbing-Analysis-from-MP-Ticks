
'''
author: Adam Forestier
date: March 28, 2023
description: email.py manages function calls for sending emails
'''
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

from my_credentials import (
    EMAIL, 
    EMAIL_PASSWORD
)
from users.user import MpUser

# Constants
PORT = 587
HOST = 'smtp.gmail.com'
EMAIL_SUBJECT = 'Montly Climbing Analysis'
MESSAGE_BODY = '''Howdy!

Attached is your monthly climbing analysis

Best,
Adam
'''


def send_mail(user: MpUser) -> None:
    '''
    arguments: MpUser object
    returns: None
    Description: send_email sends an email to user containing a zip file with all user data and graph files
    '''
    msg = MIMEMultipart()
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL
    msg['To'] = user.email
    msg.attach(body_part)
    parent_dir = 'user_files/'
    user_folder = str(user.username)
    path = os.path.join(parent_dir, user_folder)
    zip_path = f'{path}.zip'
    with open(zip_path,'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name=zip_path))

    smtp_obj = smtplib.SMTP(host=HOST, port=PORT)
    smtp_obj.starttls()
    smtp_obj.login(EMAIL, EMAIL_PASSWORD)

    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()
    return