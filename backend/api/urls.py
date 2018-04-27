from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"roadsegments", views.RoadSegmentViewSet, "roadsegment")
router.register(r"prod-data", views.ProductionDataViewSet, "productiondata")
router.register(r"users", views.UserViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    url(r"api/", include(router.urls)),
    url(r'^docs/', include_docs_urls(title='VAPI Documentation'))
]
