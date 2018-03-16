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

from api.models import RoadSegment


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ('url', 'time', 'startlat', 'startlong', 'endlat', 'endlong', 'torrsprederaktiv', 'plogaktiv',
                  'vatsprederaktiv', 'materialtype_kode', 'from_vegref', 'to_vegref', 'name', 'description')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
