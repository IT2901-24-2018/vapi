from rest_framework import serializers
from api.models import RoadSegment
from django.contrib.auth.models import User


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ('time', 'startlat', 'startlong', 'endlat', 'endlong', 'torrsprederaktiv', 'plogaktiv',
                  'vatsprederaktiv', 'materialtype_kode', 'from_vegref', 'to_vegref', 'name', 'description')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
