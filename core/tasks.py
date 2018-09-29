from celery import shared_task

from .emails import send_reset_password_email


@shared_task(serializer='pickle')
def send_reset_password_email_to_user(subject, body, from_email, to_email,
                              context, html_email_template_name):
    send_reset_password_email(subject, body, from_email, to_email,
                              context, html_email_template_name)
