from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import ProductionData
from api.serializers import ProductionDataSerializer


class InsertOneProductionDataTest(APITestCase):
    """
    Test ProductionData model.
    """
    def setUp(self):
        ProductionData.objects.create(
            time=timezone.now(), startlat=60.7758584, startlong=20.756444, endlat=60.45454, endlong=20.57575,
            plow_active=True
        )

    def test_prod_data(self):
        """
        Check that there is one and only one item in prod-data table
        """
        self.assertEqual(ProductionData.objects.count(), 1)

    def test_boolean_fields(self):
        """
        Test the boolean fields
        """
        prod_data = ProductionData.objects.all()

        # run test on the different optional fields
        self.assertEqual(prod_data[0].plow_active, True)
        self.assertIsNone(prod_data[0].dry_spreader_active)
        self.assertIsNone(prod_data[0].wet_spreader_active)
        self.assertIsNone(prod_data[0].brush_active)
        self.assertIsNone(prod_data[0].material_type_code)


class GetAllProductionDataTest(APITestCase):
    """
    Test module for GET all prod data API
    """
    def setUp(self):
        # Set up users
        User.objects.create_user(username="normal_user", password="testpassword")
        User.objects.create_user(username="staff", password="testpassword", is_staff=True)

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

    def test_get_all_prod_data_authenticated_staff(self):
        """
        Test GET request while authenticated as staff
        """
        self.client.login(username='staff', password='testpassword')

        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Get data from db and run test
        prod_data = ProductionData.objects.all()
        serializer = ProductionDataSerializer(prod_data, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_prod_data_authenticated(self):
        """
        Test GET request while authenticated, but not staff
        """
        self.client.login(username='normal_user', password='testpassword')

        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Run test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_prod_data_not_authenticated(self):
        """
        Test GET request while not authenticated
        """
        # Create instance of GET request
        url = reverse('productiondata-list')
        response = self.client.get(url)

        # Run test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostProductionDataTest(APITestCase):
    """
    Tests for posting data to the production data endpoint.
    """
    def setUp(self):
        # Make users
        User.objects.create_user(username="normal_user", password="testpassword")
        User.objects.create_user(username="staff", password="testpassword", is_staff=True)

        # Make the test data
        self.data = [{
            "time": "2018-02-02T00:00:00", "startlat": 60.7758584, "startlong": 20.756444, "endlat": 60.45454,
            "endlong": 20.57575, "plow_active": True
        }, {
            "time": "2018-02-02T00:01:00", "startlat": 60.4564577, "startlong": 20.465565, "endlat": 60.646566,
            "endlong": 20.45645, "plow_active": True
        }, {
            "time": "2018-02-02T00:02:00", "startlat": 60.56345345, "startlong": 20.3453453, "endlat": 60.3453453,
            "endlong": 20.4354, "wet_spreader_active": True
        }]

    def test_post_prod_data_list_authenticated(self):
        """
        Testing that the endpoint takes in correctly formatted data and stores it in db.
        """
        # Authenticate user
        self.client.login(username="normal_user", password="testpassword")

        # Post the data
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        # Check the status code, then check that the number of objects in the database matches the number
        # of objects in the POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionData.objects.count(), len(self.data))

    def test_post_prod_data_list_authenticated_staff(self):
        """
        Testing that the endpoint takes in correctly formatted data and stores it in db.
        """
        # Authenticate user
        self.client.login(username="staff", password="testpassword")

        # Post the data
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        # Check the status code, then check that the number of objects in the database matches the number
        # of objects in the POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionData.objects.count(), len(self.data))

    def test_post_prod_data_list_unauthenticated(self):
        """
        Testing that the endpoint has the correct restrictions on permissions.
        """
        url = reverse('productiondata-list')
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
