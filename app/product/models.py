import uuid
from django.db import models
from django.contrib.auth.models import User
from product import choices
from product.utils import generate_unique_slug


class AuditableModel(models.Model):
    """
    An abstract base class model that includes audit fields:
    - self-updating `created_at` and `updated_at` fields
    - `created_by` and `last_updated_by` to track the user creating and updating records
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_updated")

    class Meta:
        abstract = True


class Category(AuditableModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, max_length=200)

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, 'title', 'slug')
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(AuditableModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=choices.STATE_CHOICES, default=choices.DRAFT, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, 'title', 'slug')
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
