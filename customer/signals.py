# # signals.py
# import logging
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import Customer
# from customer_log.models import Customer_log
# from django.contrib.auth import get_user_model

# User = get_user_model()
# logger = logging.getLogger(__name__)

# @receiver(pre_save, sender=Customer)
# def create_customer_log(sender, instance, **kwargs):
#     if hasattr(instance, '_handled'):
#         return
#     else:
#         instance._handled = True
#     user = kwargs.get('user', None)
#     logger.info(f"Signal received for Customer ID {instance.id} (User: {user})")
#     if instance.id and user:
#         try:
#             # Retrieve the previous instance from the database
#             previous_instance = sender.objects.get(pk=instance.id)
#         except sender.DoesNotExist:
#             logger.warning(f"Previous instance not found for Customer ID {instance.id}")
#             return

#         # previous_instance = sender.objects.get(pk=instance.id)

#         # Compare the previous state with the current state
#         changed_data = {}
#         for field in instance._meta.fields:
#             field_name = field.name
#             previous_value = getattr(previous_instance, field_name)
#             current_value = getattr(instance, field_name)

#             logger.info(f"Comparing field: {field_name}")
#             logger.info(f"Previous value: {previous_value}")
#             logger.info(f"Current value: {current_value}")

#             if previous_value != current_value:
#                 changed_data[field_name] = {
#                     'previous': previous_value,
#                     'current': current_value,
#                 }

#                 logger.info(f"Changed data: {changed_data}")

#             # if getattr(previous_instance, field_name) != getattr(instance, field_name):
#             #     changed_data[field_name] = {
#             #         'previous': getattr(previous_instance, field_name),
#             #         'current': getattr(instance, field_name),
#             #     }
#             #     logger.info(f"Changed data: {changed_data}")
#                 if changed_data:
#                     formatted_remark = f"{field_name}: {changed_data[field_name]['previous']} -> {changed_data[field_name]['current']}"
#                     log_data = {
#                         'customer': instance,
#                         # 'remark': instance.__dict__,
#                         'remark':formatted_remark,
#                         'user': user#.email if user else None  # Change this based on how you want to store user information
#                     }
#                 # Create a CustomerLog instance whenever a Customer is updated
#                 # Customer_log.objects.create(customer=instance, remark=instance.__dict__)
#                     Customer_log.objects.create(**log_data)
#                     logger.info("Log entry created.")
#     else:
#         logger.warning("Signal handler conditions not met.")
# @receiver(post_save, sender=Customer)
# def create_customer_log(sender, instance,user, **kwargs):
#     if hasattr(instance, '_handled'):
#         return
#     else:
#         instance._handled = True

#     # user = kwargs.get('user', None)
#         puser=user
#     logger.info(f"Signal received for Customer ID {instance.id} (User: {puser})")

#     if instance.id and puser:
#         try:
#             # Retrieve the previous instance from the database
#             previous_instance = sender.objects.get(pk=instance.id)
#         except sender.DoesNotExist:
#             logger.warning(f"Previous instance not found for Customer ID {instance.id}")
#             return

#         changed_data = {}
#         for field in instance._meta.fields:
#             field_name = field.name
#             previous_value = getattr(previous_instance, field_name)
#             current_value = getattr(instance, field_name)

#             logger.info(f"Comparing field: {field_name}")
#             logger.info(f"Previous value: {previous_value}")
#             logger.info(f"Current value: {current_value}")

#             if previous_value != current_value:
#                 changed_data[field_name] = {
#                     'previous': previous_value,
#                     'current': current_value,
#                 }

#         if changed_data:
#             log_data = {
#                 'customer': instance,
#                 'remark': ', '.join([f"{key}: {value['previous']} -> {value['current']}" for key, value in changed_data.items()]),
#                 'user': user.email if user.email else None  # Change this based on how you want to store user information
#             }
#             # Create a CustomerLog instance whenever a Customer is updated
#             Customer_log.objects.create(**log_data)
#             logger.info("Log entry created.")
#     else:
#         logger.warning("Signal handler conditions not met.")
