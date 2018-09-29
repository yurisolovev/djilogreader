from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_reset_password_email(subject, body, from_email, to_email, context, html_email_template_name=None):
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()
