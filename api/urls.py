from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views

app_name = 'api'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/roadsegments', views.RoadSegmentViewSet)
router.register(r'api/users', views.UserViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
