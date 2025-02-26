import os
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import HydroponicSystem, SensorMeasurement

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
OTHER_USERNAME = os.getenv("OTHER_USERNAME")
OTHER_PASSWORD = os.getenv("OTHER_PASSWORD")


class HydroponicSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.other_user = User.objects.create_user(username=OTHER_USERNAME, password=OTHER_PASSWORD)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')

    def test_create_hydroponic_system(self):
        """Test successful system creation"""
        response = self.client.post(f"{BASE_URL}/api/systems/", {'name': 'New System'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def test_create_hydroponic_system_without_name(self):
        """Test creating a system without a name (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/systems/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_hydroponic_systems(self):
        """Test retrieving the list of systems (should be paginated)"""
        response = self.client.get(f"{BASE_URL}/api/systems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)  # Should return only user’s system

    def test_update_hydroponic_system(self):
        """Test updating a system name"""
        response = self.client.patch(f"{BASE_URL}/api/systems/{self.system.id}/", {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.system.refresh_from_db()
        self.assertEqual(self.system.name, 'Updated Name')

    def test_update_other_user_system(self):
        """Test updating another user’s system (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        response = self.client.patch(f"{BASE_URL}/api/systems/{other_system.id}/", {'name': 'Hacked Name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hydroponic_system(self):
        """Test deleting a system"""
        response = self.client.delete(f"{BASE_URL}/api/systems/{self.system.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HydroponicSystem.objects.count(), 0)

    def test_delete_other_user_system(self):
        """Test deleting another user’s system (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        response = self.client.delete(f"{BASE_URL}/api/systems/{other_system.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_hydroponic_system_by_id(self):
        """Test retrieving a system by ID"""
        response = self.client.get(f"{BASE_URL}/api/systems/{self.system.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test System")

    def test_get_other_user_system_by_id(self):
        """Test retrieving another user's system (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        response = self.client.get(f"{BASE_URL}/api/systems/{other_system.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_duplicate_system_name(self):
        """Test creating a system with a duplicate name (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/systems/", {'name': 'Test System'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # If uniqueness is enforced

    def test_pagination_of_systems(self):
        """Test paginated response when listing systems"""
        for i in range(15):  # Create more systems
            HydroponicSystem.objects.create(owner=self.user, name=f"System {i}")

        response = self.client.get(f"{BASE_URL}/api/systems/?page=1&page_size=10")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # Should return 10 per page

    def test_rate_limiting(self):
        """Test making too many requests (should be rate-limited if enabled)"""
        for _ in range(50):  # Simulate multiple requests
            response = self.client.get(f"{BASE_URL}/api/systems/")
            if response.status_code == 429:  # 429 Too Many Requests
                self.assertEqual(response.status_code, 429)
                break
        self.assertEqual(response.status_code, 200)

    def test_no_rate_limiting(self):
        """Test that making multiple requests does not trigger rate limiting"""
        for _ in range(20):  # Simulate 20 requests
            response = self.client.get(f"{BASE_URL}/api/systems/")
            self.assertEqual(response.status_code, 200)

    def test_hydroponic_system_str(self):
        """Test string representation of HydroponicSystem"""
        self.assertEqual(str(self.system), "Test System")

    def test_get_queryset_anonymous_user(self):
        """Test that anonymous users cannot access hydroponic systems (should return empty set)"""
        self.client.logout()
        response = self.client.get(f"{BASE_URL}/api/systems/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset_anonymous_user(self):
        """Test that anonymous users cannot access hydroponic systems (should return empty set)"""
        self.client.logout()
        response = self.client.get(f"{BASE_URL}/api/systems/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SensorMeasurementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.other_user = User.objects.create_user(username=OTHER_USERNAME, password=OTHER_PASSWORD)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')
        self.measurement = SensorMeasurement.objects.create(system=self.system, ph=6.5, temperature=22.0, tds=500)

    def test_create_measurement(self):
        """Test adding a sensor measurement"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorMeasurement.objects.count(), 2)

    def test_create_measurement_invalid_ph(self):
        """Test adding a measurement with invalid pH (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': -1.0,  # Invalid pH value
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_measurements(self):
        """Test retrieving a list of measurements"""
        response = self.client.get(f"{BASE_URL}/api/measurements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_measurements(self):
        """Test filtering measurements by pH"""
        response = self.client.get(f"{BASE_URL}/api/measurements/?ph=6.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_measurement(self):
        """Test deleting a measurement"""
        response = self.client.delete(f"{BASE_URL}/api/measurements/{self.measurement.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorMeasurement.objects.count(), 0)

    def test_create_measurement_extreme_values(self):
        """Test adding a measurement with extreme values (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 15.0,  # Invalid pH value
            'temperature': -50.0,  # Unrealistic temperature
            'tds': 100000  # Too high TDS value
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_measurement_creation(self):
        """Test creating a measurement without authentication (should fail)"""
        self.client.logout()
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_measurements_multiple_criteria(self):
        """Test filtering measurements by multiple fields"""
        SensorMeasurement.objects.create(system=self.system, ph=7.2, temperature=25.0, tds=700)
        response = self.client.get(f"{BASE_URL}/api/measurements/?ph=7.2&temperature=25.0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_measurement_invalid_system(self):
        """Test creating a measurement for a non-existent system (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': 99999,  # Invalid system ID
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_other_user_measurement(self):
        """Test deleting another user’s measurement (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        other_measurement = SensorMeasurement.objects.create(system=other_system, ph=6.5, temperature=22.0, tds=500)

        response = self.client.delete(f"{BASE_URL}/api/measurements/{other_measurement.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bulk_measurement_creation(self):
        """Test API performance by creating multiple measurements"""
        for i in range(50):  # Create 50 measurements
            SensorMeasurement.objects.create(system=self.system, ph=7.0, temperature=25.0, tds=600)

        # Request with increased page size to fetch all results
        response = self.client.get(f"{BASE_URL}/api/measurements/?page_size=50")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 50)  # Expecting at least 50 results

    def test_create_measurement_invalid_data(self):
        """Test creating a measurement with invalid data (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 20.0,  # Invalid pH
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)

    def test_user_registration(self):
        """Test registering a new user"""
        response = self.client.post(f"{BASE_URL}/api/register/", {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_user_registration(self):
        """❌ Test registering a user with an existing username (should fail)"""
        User.objects.create_user(username="duplicateuser", password=OTHER_PASSWORD)
        response = self.client.post(f"{BASE_URL}/api/register/", {
            'username': 'duplicateuser',
            'email': 'duplicate@example.com',
            'password': OTHER_PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_credentials(self):
        """Test login with incorrect credentials (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/token/", {
            'username': 'invaliduser',
            'password': OTHER_PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_valid_credentials(self):
        """Test login with correct credentials"""
        response = self.client.post(f"{BASE_URL}/api/token/", {
            'username': USERNAME,
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # JWT token should be returned

    def test_refresh_token(self):
        """Test refreshing an expired JWT token"""
        login_response = self.client.post(f"{BASE_URL}/api/token/", {
            'username': USERNAME,
            'password': PASSWORD
        })
        refresh_token = login_response.data["refresh"]

        response = self.client.post(f"{BASE_URL}/api/token/refresh/", {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Should return new access token

    def test_unauthenticated_access_to_protected_endpoint(self):
        """Test accessing a protected endpoint without authentication"""
        self.client.logout()
        response = self.client.get(f"{BASE_URL}/api/systems/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
