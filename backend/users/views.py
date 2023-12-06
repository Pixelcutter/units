from rest_framework import generics
from .models import UnitsUser
from .serializers import UnitsUserSerializer
import logging

logger = logging.getLogger("debug_to_stdout")


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UnitsUserSerializer

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
