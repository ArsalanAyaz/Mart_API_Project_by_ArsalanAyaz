import emails 
from app import settings 



def send_email_notification(*,email_to:str,subject:str,email_content_for_send:str)->None:
    # assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        text=email_content_for_send,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)

    print(f"response {response}")