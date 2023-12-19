from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    owner_id = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    quantity = models.IntegerField(default=0)
    for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    image_url = models.URLField(blank=True, null=True)
    objects = models.Manager()  # default manager

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.name
