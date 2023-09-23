import smtplib, ssl
from email.mime.text import MIMEText

# DEF: sends e-mail
def send_email(subject, body, sender, recipients, password, smtp):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp, 465, context=context) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        
        return "E-mail sent! (from: " + sender + " to " + ', '.join(recipients) + ")"