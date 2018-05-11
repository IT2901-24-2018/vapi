"""
A serializer allow complex data such as model instances to be converted to native Python
data types that can be rendered into html or json. It also provide deserialization, allowing
data to be converted back to complex data.
More info at: http://www.django-rest-framework.org/api-guide/serializers/

In each serializer is listed all the fields that are used from the model.
Also includes a url field.
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from api.models import ProductionData, RoadSegment, WeatherData


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ("url", "id", "county", "href",
                  "category", "municipality", "startdate", "region", "status",
                  "stretchdistance", "typeofroad", "roadsectionid", "vrefshortform", "the_geom")


class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = ("created", "updated", "time", "startlat", "startlong", "start_point", "endlat", "endlong",
                  "end_point", "dry_spreader_active", "plow_active", "wet_spreader_active", "brush_active",
                  "material_type_code", "segment")


class ProductionDataInputSerializer(serializers.Serializer):
    """
    Serializer for validating the input of the production data endpoint
    Does not need the save and update methods
    """
    time = serializers.DateTimeField(help_text="When the production data was generated. Example: 2016-11-04T08:45:15")
    startlat = serializers.FloatField(help_text="Start latitude. Example: 63.3870750023729")
    startlong = serializers.FloatField(help_text="Start longitute. Example: 10.3277250005425")
    endlat = serializers.FloatField(help_text="End latitude. Example: 63.3874419990294")
    endlong = serializers.FloatField(help_text="End longitude. Example: 10.3290930003037")
    dry_spreader_active = serializers.NullBooleanField(required=False,
                                                       help_text="Dry spreader active boolean. Optional.")
    plow_active = serializers.NullBooleanField(required=False, help_text="Plow boolean. Optional.")
    wet_spreader_active = serializers.NullBooleanField(required=False, help_text="Wet spreader boolean. Optional.")
    brush__active = serializers.NullBooleanField(required=False, help_text="Brush boolean. Optional.")
    material_type_code = serializers.IntegerField(allow_null=True, required=False,
                                                  help_text="Material type boolean. Optional")


class WeatherDataInputSerializer(serializers.Serializer):
    """
    Serializer for validating the weather data input. Does not need the save and update methods.
    """

    start_time_period = serializers.DateTimeField(help_text="Start time for the weather period. "
                                                            "Example: 2018-12-09T08:45:15")
    end_time_period = serializers.DateTimeField(help_text="End time for the weather period. "
                                                          "Example: 2018-12-10T08:45:15")
    county_and_municipality_id = serializers.IntegerField(help_text="County and municipality number put together."
                                                                    "Example: 5001 for Trondheim")
    value = serializers.IntegerField(help_text="The amount of precipitation without the unit. Example: 2")
    degrees = serializers.IntegerField(help_text="The degree measured in celsius.")

    def validate_value(self, value):
        """
        Checks that value is below 0
        """
        if value < 0:
            raise serializers.ValidationError("The value must be above 0.")
        return value

    def validate_county_and_municipality_id(self, value):
        """
        Check that the county and municipality id is not below 0.
        """
        if value < 0:
            raise serializers.ValidationError("The value must be above 0.")
        return value

    def validate(self, data):
        """
        Checks multiple time cases
        """
        if data['start_time_period'] > data['end_time_period']:
            raise serializers.ValidationError("End time can not be before start time")
        elif (timezone.now() - data['end_time_period']) > timedelta(days=1):
            raise serializers.ValidationError("Weather can not be over 24 hours old")
        elif data['end_time_period'] > timezone.now():
            raise serializers.ValidationError("End time can not be in the future")
        elif (data['end_time_period'] - data['start_time_period']) >= timedelta(days=1):
            raise serializers.ValidationError("Only supports 1 day time frame for weather")
        return data


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ('id', 'created', 'updated', 'start_time_period', 'end_time_period', 'county_and_municipality_id',
                  'value', 'unit', 'degrees', 'segment')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "id", "username")
