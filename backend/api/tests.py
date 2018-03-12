from django.test import TestCase, RequestFactory
from rest_framework.reverse import reverse
from django.contrib.auth.models import User, AnonymousUser
from api.views import ProductionDataViewSet
from api.models import ProductionData
from api.serializers import ProductionDataSerializer
from rest_framework import status
from django.utils import timezone


class InsertOneProductionDataTest(TestCase):
    """
    Test module for ProductionData.
    """

    def setUp(self):
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.7758584, startlong=20.756444, endlat=60.45454, endlong=20.57575,
            plow_active=True
        )

    def test_prod_data(self):
        """
        Test input of one ProductionData object
        """
        prod_data = ProductionData.objects.all()
        self.assertEqual(len(prod_data), 1)


class GetAllProductionDataTest(TestCase):
    """
    Test module for GET all prod data API
    """
    def setUp(self):
        # Set up request factory and user
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="haavahe", password="123qweasd")

        # Create data in db
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.7758584, startlong=20.756444, endlat=60.45454, endlong=20.57575,
            plow_active=True
        )
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.4564577, startlong=20.465565, endlat=60.646566, endlong=20.45645,
            plow_active=True
        )
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.56345345, startlong=20.3453453, endlat=60.3453453, endlong=20.4354,
            wet_spreader_active=True
        )

    def test_get_all_prod_data_authenticated(self):
        """
        Test GET request while authenticated
        """
        # Create instance of GET request
        request = self.factory.get(reverse('prod-data-list'))
        request.user = self.user

        # Get API response
        response = ProductionDataViewSet.as_view({'get': 'list'})(request)

        # Get data from db
        prod_data = ProductionData.objects.all()
        serializer = ProductionDataSerializer(prod_data, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_prod_data_not_authenticated(self):
        """
        Test GET request while not authenticated
        """
        # Create instance of GET request
        request = self.factory.get(reverse('prod-data-list'))
        request.user = AnonymousUser()

        # Get API response
        response = ProductionDataViewSet.as_view({'get': 'list'})(request)

        # Get data from db
        prod_data = ProductionData.objects.all()
        serializer = ProductionDataSerializer(prod_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

