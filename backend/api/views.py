from backend.settings.constants import INPUT_LIST_LIMIT
from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from api.models import ProductionData, RoadSegment
from api.permissions import IsAdminOrReadOnly, IsStaffOrCreateOnly
from api.serializers import ProductionDataSerializer, RoadSegmentSerializer, UserSerializer


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class ProductionDataViewSet(viewsets.ModelViewSet):
    """
    This viewset supports `create` and `list` actions.
    """
    queryset = ProductionData.objects.all()
    serializer_class = ProductionDataSerializer
    # Only registered users can use this view
    permission_classes = (permissions.IsAuthenticated, IsStaffOrCreateOnly,)

    def create(self, request, *args, **kwargs):
        """
        Add support for creating when the input data is a list
        """
        many = False

        # Check if the incoming data is a list
        # If it is a list set the many flag to True
        if isinstance(request.data, list):
            many = True
            if len(request.data) > INPUT_LIST_LIMIT:
                error = {"detail": "Input list too long"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # TODO: map prod data to road a road segment
        mapped_data = request.data

        # Instantiate the serializer
        serializer = self.get_serializer(data=mapped_data, many=many)

        # Check if the serializer is valid and takes the necessary actions
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
