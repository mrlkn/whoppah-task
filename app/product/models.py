from django.db import models
from django.utils.text import slugify

from product import choices
from product.utils import generate_unique_slug


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, max_length=200)

    def save(self, *args, **kwargs):
        # Auto-generate slug before saving
        if not self.slug:
            self.slug = generate_unique_slug(self, 'title', 'slug')
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=choices.STATE_CHOICES, default=choices.DRAFT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'title', 'slug')
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
