from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    color_hexcode = models.CharField(max_length=7, blank=True, null=True)
    owner_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner_id"], name="unique_category_name_owner"
            )
        ]

    def __str__(self):
        return self.name
