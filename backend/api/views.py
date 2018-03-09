from rest_framework import viewsets, permissions, status
from api.models import RoadSegment, ProductionData
from api.serializers import RoadSegmentSerializer, ProductionDataSerializer, UserSerializer
from django.contrib.auth.models import User
from api.permissions import IsAdminOrReadOnly, CreateAndListOnly
from rest_framework.response import Response


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
    permission_classes = (permissions.IsAuthenticated, CreateAndListOnly,)

    def create(self, request, *args, **kwargs):
        """
        Add support for creating when the input data is a list to the create method
        """
        many = False

        # Check if the incoming data is a list
        # If it is a list set the many flag to True
        if isinstance(request.data, list):
            many = True

        # Instantiate the serializer
        serializer = self.get_serializer(data=request.data, many=many)

        # Check if the serializer is valid and takes the necessary actions
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Deny retrieve actions. Prevent returning single prod data.
        """
        error = {"detail": "The retrieve action is not supported."}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
