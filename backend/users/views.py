from rest_framework import generics
from .models import UnitsUser
from .serializers import UnitsUserSerializer
import logging
from units_api.permissions import IsUserPermission
from rest_framework import exceptions


logger = logging.getLogger("debug_to_stdout")


class RegisterUnitsUserView(generics.CreateAPIView):
    serializer_class = UnitsUserSerializer
    permission_classes = []


class UnitsUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitsUser.objects.all()
    serializer_class = UnitsUserSerializer
    permission_classes = [IsUserPermission]
