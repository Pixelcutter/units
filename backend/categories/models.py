from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    color_hexcode = models.CharField(max_length=7, blank=True, null=True)
    category_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ("-created_at",)
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["name", "category_owner"], name="unique_category_name_owner"
    #         )
    #     ]

    def __str__(self):
        return self.name
