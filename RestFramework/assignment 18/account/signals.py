# Signals for the account app
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

# this signal will be triggered when a token is created for a user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # if a token is created, we will create a token for the user
        Token.objects.create(user=instance)