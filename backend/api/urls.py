from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'roadsegments', views.RoadSegmentViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'api/', include(router.urls))
]
