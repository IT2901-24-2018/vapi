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

from api.models import ProductionData, RoadSegment, WeatherData


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ('url', 'id', 'county', 'href',
                  'category', 'municipality', 'startdate', 'region', 'status',
                  'stretchdistance', 'typeofroad', 'roadsectionid', 'vrefshortform', 'the_geom')


class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = ('created', 'updated', 'time', 'startlat', 'startlong', 'endlat', 'endlong', 'dry_spreader_active',
                  'plow_active', 'wet_spreader_active', 'brush_active', 'material_type_code', 'segment')

class WeatherDataInputSerializer(serializers.Serializer):
    """
    Serializer for validating the weather data input. Does not need the save and update methods.
    """
    time = serializers.DateTimeField(help_text="When the weather data was generated. Example: 2018-12-09T08:45:15Z")
    county_and_municipality_id = serializers.IntegerField(help_text="County and municipality number put together."
                                                               "Example: 5001 for Trondheim")
    value = serializers.IntegerField(help_text="The amount of precipitation without the unit. Example: 2")
    unit = serializers.CharField(max_length=2, help_text="The unit describing the value. Max two in length."
                                                    "Only supports mm at the moment. Example: mm for millimeter")
    degrees = serializers.IntegerField(help_text="The degree measured in celsius.")


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ('created', 'updated', 'time', 'county_and_municipality_id', 'value', 'unit',
                  'degrees', 'segment')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
