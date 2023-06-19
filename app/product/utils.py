from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from . import choices


def generate_unique_slug(
    model_instance: models.Model, slugable_field_name: str, slug_field_name: str
) -> str:
    """
    Generate a unique slug for a given model instance.

    This function takes a model instance, the name of the field to create slug from,
    and the name of the slug field. It returns a unique slug by appending a suffix if necessary.

    Args:
        model_instance (models.Model): Instance of a Django model.
        slugable_field_name (str): Name of the field to create slug from.
        slug_field_name (str): Name of the slug field.

    Returns:
        str: Unique slug.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__

    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{extension}"
        extension += 1

    return unique_slug


def is_valid_transition(instance, new_state: str, user: User) -> bool:
    user_role = []
    if user.is_staff:
        user_role.append("admin")
    if instance.created_by == user:
        user_role.append("creator")

    allowed_transition = choices.TRANSITIONS.get(instance.state, {}).get(new_state)

    return allowed_transition in user_role
