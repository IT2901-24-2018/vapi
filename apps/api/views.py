from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from vapi.constants import INPUT_LIST_LIMIT

from api.mapper import mapper
from api.models import ProductionData, RoadSegment, WeatherData
from api.permissions import IsAdminOrReadOnly, IsStaffOrCreateOnly
from api.serializers import (ProductionDataSerializer, RoadSegmentSerializer, UserSerializer,
                             WeatherDataInputSerializer, WeatherDataSerializer)
from api.weather import weather


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `read`, 'update', 'partial_update'
    and `destroy` actions.

    list: Returns all the elements. Road segments in this case.

    read: Retrieve a road segment. #ID of the road segment needed.

    update: Update a road segment. All fields are mandatory.

    partial_update: Update a road segment. No fields are mandatory.

    destroy: Request for deleting a road segment element.
    """
    pagination_class = StandardResultsSetPagination
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        """
        Inputs a list of road segments.
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


class ProductionDataViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `read`, 'update', 'partial_update'
    and `destroy` actions.

    list: Returns all the elements. Production data in this case.

    read: Retrieve production data. #ID of the production needed.

    update: Updates one single production data. All fields are mandatory.

    partial_update: Updates one single production data. No fields are mandatory.

    destroy: Request for deleting a production data element.
    """
    queryset = ProductionData.objects.all()
    serializer_class = ProductionDataSerializer
    # Only registered users can use this view
    permission_classes = (permissions.IsAuthenticated, IsStaffOrCreateOnly,)

    def create(self, request, *args, **kwargs):
        """
        Input new production data. The data will be mapped to a road segment defined by set parameters.
        """
        data = []

        # Check if the incoming data is a list
        # If it is a list set the many flag to True

        if isinstance(request.data, list):
            data = request.data
            if len(request.data) > INPUT_LIST_LIMIT:
                error = {"detail": "Input list too long"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            data.append(request.data)

        # Map prod data to road segment
        mapped_data = mapper.map_to_segment(data)

        # Check that there are successfully mapped prod-data
        if len(mapped_data) == 0:
            error = {"detail": "No segments within range"}
            return Response(error, status=status.HTTP_200_OK)

        # Handle overlap with old prod-data
        mapped_data = mapper.handle_prod_data_overlap(mapped_data)

        # Instantiate the serializer
        serializer = self.get_serializer(data=mapped_data, many=True)

        # Check if the serializer is valid and takes the necessary actions
        if serializer.is_valid():
            # Handle weather data when adding new production data
            weather.handle_prod_weather_overlap(serializer.data)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherViewSet(viewsets.ModelViewSet):
    """
    list: Returns all the elements. Weather data in this case.

    read: Retrieve weather data. #ID of the weather needed.

    update: Updates one single weather data. All fields are mandatory.

    partial_update: Updates one single weather data. No fields are mandatory.

    destroy: Request for deleting a weather data element.
    """
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataInputSerializer
    # Only registered users can use this view
    permission_classes = (permissions.IsAuthenticated, IsStaffOrCreateOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = WeatherDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create new weather data from list mapped to road segment
        """
        data = []

        if isinstance(request.data, list):
            data = request.data
            if len(request.data) > INPUT_LIST_LIMIT:
                error = {"detail": "Input list too long"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            data.append(request.data)

        serializer = self.get_serializer(data=data, many=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Map weather data to road a road segment
        number_of_updated_weather, mapped_weather = weather.map_weather_to_segment(data)

        # Instantiate the serializer
        serializer = WeatherDataSerializer(data=mapped_weather, many=True)

        # Check if the serializer is valid and takes the necessary actions
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # headers = self.get_success_headers(serializer.data)
            return Response(
                "{} row(s) added and {} weather objects updated".format(len(serializer.data),
                                                                        number_of_updated_weather),
                status=status.HTTP_201_CREATED,
            )

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `read` actions.

    list: Lists all users.

    read: Returns the user with a given ID.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
