import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User ,Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    logger.debug(f"Signal triggered for user: {instance.username}, created: {created}, is_active: {instance.is_active}")
    if created and not instance.is_active:
        logger.debug("Preparing to send activation email")
        token = default_token_generator.make_token(instance)
        uid = instance.pk

        activation_link = f"https://django-assignment-2-5y10.onrender.com//users/activate/{uid}/{token}/"

        subject = 'Activate Your Account'
        message = f"""
        Hi {instance.username},

        Please activate your account by clicking the link below:

        {activation_link}

        Thank you!
        """

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False
            )
            logger.debug(f"Email sent to {instance.email}")
        except Exception as e:
            logger.error(f"Email sending error: {e}")