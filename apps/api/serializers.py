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
    time = serializers.DateTimeField(help_text="When the production data was generated. Example: 2016-11-04T08:45:15Z")
    startlat = serializers.FloatField(help_text="Start latitude. Example: 63.3870750023729")
    startlong = serializers.FloatField(help_text="Start longitute. Example: 10.3277250005425")
    endlat = serializers.FloatField(help_text="End latitude. Example: 63.3874419990294", required=False)
    endlong = serializers.FloatField(help_text="End longitude. Example: 10.3290930003037", required=False)
    dry_spreader_active = serializers.NullBooleanField(required=False,
                                                       help_text="Dry spreader active boolean. Optional.")
    plow_active = serializers.NullBooleanField(required=False, help_text="Plow boolean. Optional.")
    wet_spreader_active = serializers.NullBooleanField(required=False, help_text="Wet spreader boolean. Optional.")
    brush__active = serializers.NullBooleanField(required=False, help_text="Brush boolean. Optional.")
    material_type_code = serializers.IntegerField(allow_null=True, required=False,
                                                  help_text="Material type boolean. Optional")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "id", "username")
