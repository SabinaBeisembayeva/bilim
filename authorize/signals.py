from django.db.models.signals import post_save
from django.dispatch import receiver

from authorize.models import User

@receiver(post_save, sender=User)
def sending_activation(created, instance, **kwargs):
    """Send the activation template to the user's email!"""
    from authorize.services.user_mail import sending_activation_template_to_user

    if created:
        from django.utils import timezone
        instance.created_at = timezone.now()
        instance.save()
        sending_activation_template_to_user(instance)
