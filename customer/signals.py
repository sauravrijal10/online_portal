# # signals.py
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Customer
from customer_log.models import Customer_log
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Customer)
def capture_previous_values(sender, instance, **kwargs):
    if not instance.pk:
        return  

    try:
        previous_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return 

    instance._previous_values = {field.name: getattr(previous_instance, field.name) for field in instance._meta.fields}

@receiver(post_save, sender=Customer)
def create_customer_log(sender, instance, **kwargs):
    if hasattr(instance, '_handled'):
        return
    else:
        instance._handled = True

    logger.info(f"Signal received for Customer ID {instance.id}") 

    if instance.id: 
        previous_values = getattr(instance, '_previous_values', {})

        changed_data = {}
        for field in instance._meta.fields:
            field_name = field.name
            previous_value = previous_values.get(field_name, None)
            current_value = getattr(instance, field_name)

            previous_value_stripped = str(previous_value).strip().lower()
            current_value_stripped = str(current_value).strip().lower()

            logger.info(f"Comparing field: {field_name}")
            logger.info(f"Previous value: {previous_value}")
            logger.info(f"Current value: {current_value}")

            if previous_value_stripped != current_value_stripped:
                changed_data[field_name] = {
                    'previous': previous_value,
                    'current': current_value,
                }

        if changed_data:
           

            log_data = {
                'customer': instance,
                'remark': ', '.join([f"{key}: {value['previous']} -> {value['current']}" for key, value in changed_data.items()]),
                
            }
            Customer_log.objects.create(**log_data)
            logger.info("Log entry created.")
    else:
        logger.warning("Signal handler conditions not met.")