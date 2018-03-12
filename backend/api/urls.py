from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'roadsegments', views.RoadSegmentViewSet, 'roadsegments')
# router.register(r'productiondata', views.ProductionDataViewSet)
# or
router.register(r'prod-data', views.ProductionDataViewSet, 'prod-data')
router.register(r'users', views.UserViewSet, 'users')

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r'api/', include(router.urls))
]
