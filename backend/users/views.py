from rest_framework import generics
from .models import UnitsUser
from .serializers import UnitsUserSerializer
import logging
from units_api.permissions import IsUserPermission
from rest_framework import exceptions


logger = logging.getLogger("debug_to_stdout")


class RegisterUnitsUserView(generics.CreateAPIView):
    serializer_class = UnitsUserSerializer


class UnitsUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitsUser.objects.all()
    serializer_class = UnitsUserSerializer

    # check if authenticated user is user being requested
    # permission_classes = [IsUserPermission]

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != int(kwargs["pk"]):
            logger.debug("User is not owner of requested user")
            return exceptions.PermissionDenied

        return super().dispatch(request, *args, **kwargs)
