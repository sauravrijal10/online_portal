from django.contrib.auth.tokens import default_token_generator
from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.models import Site



@shared_task
def send_activation_email(user, current_site_domain):
    # current_site = Site.objects.get_current()
    mail_subject = 'Activate your account'
    mail_subject = 'Activate your account'
    activation_link = f"http://{current_site_domain}/api/user/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
    message = f"Hi {user.username},\n\nClick the following link to activate your account:\n\n{activation_link}"
    send_mail(mail_subject, message, 'your-email@example.com', [user.email])
    print(user.email)