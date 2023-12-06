from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User_Credentials, Deal

#Order Fetching Modules
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received

@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    # Create groups for the new user model
    group, created = Group.objects.get_or_create(name='admin')
    group, created = Group.objects.get_or_create(name='editor')

    # Create permissions for the new user model
    content_type = ContentType.objects.get_for_model(User_Credentials)
    permissions = Permission.objects.filter(content_type=content_type)

    # Assign the permissions to the groups
    for permission in permissions:
        group.permissions.add(permission)

@receiver(valid_ipn_received)
def valid_ipn(sender,**kwargs):
    ipn = sender
    print("IPN VALID")
    if ipn.payment_status == 'Completed':
        Deal.objects.create()



@receiver(invalid_ipn_received)
def invalid_ipn(sender,**kwargs):
    ipn = sender
    print("IPN INVALID")
    if ipn.payment_status == 'Completed':
        Deal.objects.create()