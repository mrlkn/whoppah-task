from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import send_email_task


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    """
    Handles the post_save signal of the Product model.

    Args:
        sender (Model): The model class.
        instance (Product): The actual instance being saved.
        **kwargs: Arbitrary keyword arguments.
    """

    state_message_map = {
        'rejected': 'Your product has been rejected.',
        'banned': 'Your product has been banned.',
        'accepted': 'Your product has been accepted.'
    }

    if instance.state in state_message_map:
        subject = f"Product {instance.state.capitalize()}"
        message = state_message_map[instance.state]
        recipient_email = instance.created_by.email
        send_email_task.delay(recipient_email, subject, message)
