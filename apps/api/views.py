from django.db import connection
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from vapi.constants import INPUT_LIST_LIMIT, MAX_SEGMENT_LENGTH, MIN_COORDINATES_LENGTH

from api.mapper.mapper import map_to_segment
from api.models import ProductionData, RoadSegment, WeatherData
from api.overlap_handler.overlap_handler import handle_prod_data_overlap
from api.permissions import IsAdminOrReadOnly, IsStaffOrCreateOnly
from api.segmenter.road_segmenter import segment_network
from api.serializers import (ProductionDataInputSerializer, ProductionDataSerializer,
                             RoadSegmentSerializer, WeatherDataInputSerializer,
                             WeatherDataSerializer)
from api.weather import weather


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides "list", "create", "read", "update", "partial_update"
    and "destroy" actions.

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
        data = []

        # Check if the incoming data is a list
        # If it is a list set the many flag to True
        if isinstance(request.data, list):
            data = request.data
        else:
            data.append(request.data)

        # segment stuff here
        segments = segment_network(data, MAX_SEGMENT_LENGTH, MIN_COORDINATES_LENGTH)

        # Instantiate the serializer
        serializer = self.get_serializer(data=segments, many=True)

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
    This viewset automatically provides "list", "create", "read", "update", "partial_update"
    and "destroy" actions.

    list: Returns all the elements. Production data in this case.

    read: Retrieve production data. #ID of the production needed.

    update: Updates one single production data. All fields are mandatory.

    partial_update: Updates one single production data. No fields are mandatory.

    destroy: Request for deleting a production data element.
    """
    queryset = ProductionData.objects.all()
    serializer_class = ProductionDataInputSerializer
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

        serializer = self.get_serializer(data=data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Map production data to a road segment
        mapped_data = map_to_segment(data)

        # Check that there are successfully mapped prod-data
        if len(mapped_data) == 0:
            error = {"detail": "No segments within range"}
            return Response(error, status=status.HTTP_200_OK)

        # Handle overlap with old prod-data
        mapped_data = handle_prod_data_overlap(mapped_data)

        # Instantiate the serializer
        serializer = ProductionDataSerializer(data=mapped_data, many=True)

        # Check if the serializer is valid and takes the necessary actions
        if serializer.is_valid():
            # Handle weather data when adding new production data
            weather.handle_prod_weather_overlap(serializer.validated_data)
            serializer.save()
            return Response(
                "{} row(s) added".format(len(serializer.data)),
                status=status.HTTP_201_CREATED,
            )

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductionDataSerializer(queryset, many=True)
        return Response(serializer.data)


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
            return Response(
                "{} row(s) added and {} weather objects updated".format(len(serializer.data),
                                                                        number_of_updated_weather),
                status=status.HTTP_201_CREATED,
            )

        # If not valid return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SegmentStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for status on segments
    """
    pagination_class = StandardResultsSetPagination
    page_size = 100

    def get_queryset(self):
        """
        Django Rest Framework complains if this is not overridden
        """
        pass

    def get_queryset_custom(self, segment_id=None, page=None, page_size=None):
        """
        Custom method for getting the query data
        Uses raw sql as the query is a bit difficult to implement with django models
        :param segment_id: id of the segment for retrieve
        :param page: page number for list
        :param page_size: page size for list
        :return: When used by retrieve, a dictionary. When used by list, a list of dictionaries
        """
        with connection.cursor() as cursor:
            stmt = """
            SELECT s.id, s.county, s.href, s.category, s.municipality, s.region,
            s.status, s.stretchdistance, s.typeofroad, s.roadsectionid, s.vrefshortform,
            (SELECT ST_AsText(s.the_geom)) AS the_geom,
            w.start_time_period, w.end_time_period,
            w.value, w.unit, w.degrees,

            (SELECT MAX(p.time) FROM api_productiondata AS p WHERE p.segment_id = s.id) AS time,
            (SELECT EXISTS
              (SELECT * FROM api_productiondata AS p
              WHERE p.segment_id = s.id AND p.dry_spreader_active = TRUE)) AS dry_spreader_active,
            (SELECT EXISTS
              (SELECT * FROM api_productiondata AS p
              WHERE p.segment_id = s.id AND p.plow_active = TRUE)) AS plow_active,
            (SELECT EXISTS
              (SELECT * FROM api_productiondata AS p
              WHERE p.segment_id = s.id AND p.wet_spreader_active = TRUE)) AS wet_spreader_active,
            (SELECT EXISTS
              (SELECT * FROM api_productiondata AS p
              WHERE p.segment_id = s.id AND p.brush_active = TRUE)) AS brush_active,
            (SELECT p.material_type_code
              FROM api_productiondata AS p
              WHERE p.segment_id = s.id ORDER BY p.material_type_code LIMIT 1) AS material_type_code

            FROM api_roadsegment AS s
            INNER JOIN api_weatherdata AS w ON s.id = w.segment_id
            """
            if segment_id is not None:
                where_clause = "WHERE s.id = %s"
                cursor.execute(stmt + where_clause, [segment_id])
                columns = [col[0] for col in cursor.description]
                rows = dict(zip(columns, cursor.fetchone()))
            else:
                if page is not None and page_size is not None:
                    pagination = "LIMIT %s OFFSET %s"
                    cursor.execute(stmt + pagination, [page_size, (int(page) - 1) * int(page_size)])
                else:
                    pagination = "LIMIT %s"
                    cursor.execute(stmt + pagination, [page_size])
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows

    def list(self, request, *args, **kwargs):
        """
        List all segments with status.
        Defaults to 100 segments
        Use: /api/road-status/?page=<page_number>&page_size<number_of_segments_per_page>
        """
        page = request.query_params.get("page", None)
        if request.query_params.get("page_size", None) is not None:
            page_size = request.query_params.get("page_size", None)
        else:
            page_size = self.page_size
        if page is not None and page_size is not None:
            return Response(self.get_queryset_custom(page=page, page_size=page_size))

        return Response(self.get_queryset_custom(page_size=self.page_size))

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve one segment with status from pk
        """
        return Response(self.get_queryset_custom(segment_id=pk))
