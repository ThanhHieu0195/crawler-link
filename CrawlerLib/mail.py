from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from Configs.enum import ServerConfig

def send_mail(to, subject, content):
    message = Mail(
            from_email='crawler@viralworks.com',
            to_emails=to,
            subject=subject,
            html_content=content)
    try:
        api_key=ServerConfig.SENDGRID_KEY.value
        sg = SendGridAPIClient(api_key)
        return sg.send(message)
    except Exception as e:
        print(e)
    return False

