from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, permissions
from api.models import RoadSegment
from api.serializers import RoadSegmentSerializer
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from api.permissions import IsAdminOrReadOnly


@api_view
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'roadsegments': reverse('roadsegment-list', request=request, format=format)
    })


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
