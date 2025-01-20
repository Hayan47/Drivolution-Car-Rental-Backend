from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to Drivolution',
            'Thank for signing up!',
            'admin@drivolution.com',
            [instance.email],
            fail_silently=False,
        )
