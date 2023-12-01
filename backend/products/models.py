from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from categories.models import Category


class Product(models.Model):
    class ProductObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(for_sale=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    for_sale = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    image_url = models.URLField(blank=True, null=True)
    objects = models.Manager()  # default manager
    productobjects = ProductObjects()  # custom manager

    class Meta:
        ordering = ("created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "product_owner"], name="unique_product_name_owner"
            )
        ]

    def __str__(self):
        return self.name
