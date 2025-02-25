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


class HydroponicSystemTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.other_user = User.objects.create_user(username="otheruser", password="password123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')

    def test_create_hydroponic_system(self):
        """✅ Test successful system creation"""
        response = self.client.post(f"{BASE_URL}/api/systems/", {'name': 'New System'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def test_create_hydroponic_system_without_name(self):
        """❌ Test creating a system without a name (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/systems/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_hydroponic_systems(self):
        """✅ Test retrieving the list of systems (should be paginated)"""
        response = self.client.get(f"{BASE_URL}/api/systems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)  # Should return only user’s system

    def test_update_hydroponic_system(self):
        """✅ Test updating a system name"""
        response = self.client.patch(f"{BASE_URL}/api/systems/{self.system.id}/", {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.system.refresh_from_db()
        self.assertEqual(self.system.name, 'Updated Name')

    def test_update_other_user_system(self):
        """❌ Test updating another user’s system (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        print(other_system)
        print(other_system.id)
        response = self.client.patch(f"{BASE_URL}/api/systems/{other_system.id}/", {'name': 'Hacked Name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hydroponic_system(self):
        """✅ Test deleting a system"""
        response = self.client.delete(f"{BASE_URL}/api/systems/{self.system.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HydroponicSystem.objects.count(), 0)

    def test_delete_other_user_system(self):
        """❌ Test deleting another user’s system (should fail)"""
        other_system = HydroponicSystem.objects.create(owner=self.other_user, name="Other System")
        response = self.client.delete(f"{BASE_URL}/api/systems/{other_system.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SensorMeasurementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')
        self.measurement = SensorMeasurement.objects.create(system=self.system, ph=6.5, temperature=22.0, tds=500)

    def test_create_measurement(self):
        """✅ Test adding a sensor measurement"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorMeasurement.objects.count(), 2)

    def test_create_measurement_invalid_ph(self):
        """❌ Test adding a measurement with invalid pH (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': -1.0,  # Invalid pH value
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_measurements(self):
        """✅ Test retrieving a list of measurements"""
        response = self.client.get(f"{BASE_URL}/api/measurements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_measurements(self):
        """✅ Test filtering measurements by pH"""
        response = self.client.get(f"{BASE_URL}/api/measurements/?ph=6.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_measurement(self):
        """✅ Test deleting a measurement"""
        response = self.client.delete(f"{BASE_URL}/api/measurements/{self.measurement.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorMeasurement.objects.count(), 0)


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """✅ Test registering a new user"""
        response = self.client.post(f"{BASE_URL}/api/register/", {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_user_registration(self):
        """❌ Test registering a user with an existing username (should fail)"""
        User.objects.create_user(username="duplicateuser", password="password123")
        response = self.client.post(f"{BASE_URL}/api/register/", {
            'username': 'duplicateuser',
            'email': 'duplicate@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_credentials(self):
        """❌ Test login with incorrect credentials (should fail)"""
        response = self.client.post(f"{BASE_URL}/api/token/", {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
