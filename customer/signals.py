# # signals.py
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Customer
from customer_log.models import Customer_log
from online_portal.middleware import get_current_user
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

    instance._previous_status = getattr(previous_instance, 'status', None)

@receiver(post_save, sender=Customer)
def create_customer_log(sender, instance, **kwargs):
    if hasattr(instance, '_handled'):
        return
    else:
        instance._handled = True

    logger.info(f"Signal received for Customer ID {instance.id}") 

    if instance.id: 
        previous_status = getattr(instance, '_previous_status', None)
        current_status = instance.status

        if previous_status is None:
            previous_status = 'None'

        previous_status_stripped = str(previous_status).strip().lower()
        current_status_stripped = str(current_status).strip().lower()
        print(previous_status)
           
        if previous_status_stripped != current_status_stripped:
            user = get_current_user()
            log_data = {
                'customer': instance,
                'remark': f"status: {previous_status} -> {current_status}",
                'user':user,

                
            }
            if previous_status != 'None':
                Customer_log.objects.create(**log_data)
                logger.info("Log entry created.")
    else:
        logger.warning("Signal handler conditions not met.")