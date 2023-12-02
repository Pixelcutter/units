from django.db import models


class UserIsOwnerMixin:
    user_field = "owner_id"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user.id
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)

        return qs.filter(**lookup_data)
