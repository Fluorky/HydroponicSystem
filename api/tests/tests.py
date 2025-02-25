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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')

    def test_create_hydroponic_system(self):
        response = self.client.post(f"{BASE_URL}/api/systems/", {'name': 'New System'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def test_list_hydroponic_systems(self):
        response = self.client.get(f"{BASE_URL}/api/systems/")
        print("Response data:", response.data)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_hydroponic_system(self):
        response = self.client.patch(f"{BASE_URL}/api/systems/{self.system.id}/", {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.system.refresh_from_db()
        self.assertEqual(self.system.name, 'Updated Name')

    def test_delete_hydroponic_system(self):
        response = self.client.delete(f"{BASE_URL}/api/systems/{self.system.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HydroponicSystem.objects.count(), 0)


class SensorMeasurementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(owner=self.user, name='Test System')
        self.measurement = SensorMeasurement.objects.create(system=self.system, ph=6.5, temperature=22.0, tds=500)

    def test_create_measurement(self):
        response = self.client.post(f"{BASE_URL}/api/measurements/", {
            'system': self.system.id,
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 600
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorMeasurement.objects.count(), 2)

    def test_list_measurements(self):
        response = self.client.get(f"{BASE_URL}/api/measurements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_measurements(self):
        response = self.client.get(f"{BASE_URL}/api/measurements/?ph=6.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_measurement(self):
        response = self.client.delete(f"{BASE_URL}/api/measurements/{self.measurement.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorMeasurement.objects.count(), 0)


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        response = self.client.post(f"{BASE_URL}/api/register/", {
            'username': USERNAME,
            'email': 'newuser@example.com',
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=USERNAME).exists())
