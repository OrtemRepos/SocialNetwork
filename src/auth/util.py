from email.message import EmailMessage
from email.utils import make_msgid
import smtplib

from src.auth.config import config

html_msg = ''
with open('src/auth/templates/email_template.html', 'r') as f:
    html_msg = f.read()


def send_email(user_email: str, token: str):
    
    msg = EmailMessage()
    msg.set_content(html_msg.replace('target_confirm_url', f'http://localhost:3000/confirm?token={token}'))