from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_email(user_email: str, token: str, html_msg: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirm your email"
    text = f"Hello, please confirm your email\nThis your token: {token}"
    html = html_msg.replace("|token|", token)
    plain_msg = MIMEText(text, "plain")
    html_msg = MIMEText(html, "html")
    msg.attach(plain_msg)
    msg.attach(html_msg)
    return msg
