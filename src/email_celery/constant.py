html_verify_msg = ""
with open("src/email_celery/template/confirm_email.html") as f:
    html_verify_msg = f.read()
