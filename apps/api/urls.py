from django.conf.urls import include, url
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"roadsegments", views.RoadSegmentViewSet, "roadsegment")
router.register(r"prod-data", views.ProductionDataViewSet, "productiondata")
router.register(r"users", views.UserViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    # Handle api/
    url(r"api/", include(router.urls)),
    # Redirect api to api/
    url(r'^api$', RedirectView.as_view(url='/api/')),
    # Handle docs/
    url(r'^docs/', include_docs_urls(title='VAPI Documentation')),
    # Redirect docs to docs/
    url(r'^docs$', RedirectView.as_view(url='/docs/'))
]
