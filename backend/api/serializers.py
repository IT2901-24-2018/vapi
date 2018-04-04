"""
A serializer allow complex data such as model instances to be converted to native Python
data types that can be rendered into html or json. It also provide deserialization, allowing
data to be converted back to complex data.
More info at: http://www.django-rest-framework.org/api-guide/serializers/

In each serializer is listed all the fields that are used from the model.
Also includes a url field.
"""

from rest_framework import serializers
from api.models import RoadSegment
from django.contrib.auth.models import User


class RoadSegmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoadSegment
        fields = ('id', 'coordinates', 'fra_meter', 'fylke', 'srid', 'hp', 'href',
                  'kategori', 'kommune', 'konnekteringslenke', 'kortform', 'medium', 'startdato',
                  'nummer', 'region', 'sluttnode', 'sluttposisjon', 'startnode', 'startposisjon',
                  'status', 'strekningslengde', 'temakode', 'til_meter', 'typeveg', 'vegavdeling',
                  'veglenkeid', 'vrefkortform')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
