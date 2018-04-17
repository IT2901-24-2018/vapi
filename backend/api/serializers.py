"""
A serializer allow complex data such as model instances to be converted to native Python
data types that can be rendered into html or json. It also provide deserialization, allowing
data to be converted back to complex data.
More info at: http://www.django-rest-framework.org/api-guide/serializers/

In each serializer is listed all the fields that are used from the model.
Also includes a url field.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import ProductionData, RoadSegment


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ('url', 'id', 'coordinates', 'from_meter', 'county', 'srid', 'hp', 'href',
                  'category', 'municipality', 'connlink', 'shortform', 'medium', 'startdate',
                  'number', 'region', 'endnode', 'endposition', 'startnode', 'startposition',
                  'status', 'stretchdistance', 'themecode', 'to_meter', 'typeofroad', 'roadsection',
                  'roadsectionid', 'vrefshortform')


class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = ('created', 'updated', 'time', 'startlat', 'startlong', 'endlat', 'endlong', 'dry_spreader_active',
                  'plow_active', 'wet_spreader_active', 'brush_active', 'material_type_code')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')