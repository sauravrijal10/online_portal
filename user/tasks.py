# # tasks.py
# from celery import shared_task
# from .utils import send_activation_email
# from .models import User
# @shared_task
# def send_activation_email_async(user_id,current_site_domain):
#     user = User.objects.get(pk=user_id)
#     send_activation_email(user, current_site_domain)
