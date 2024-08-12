# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role

@receiver(post_migrate)
def create_admin_role(sender, **kwargs):
    Role.objects.get_or_create(nom='admin')

