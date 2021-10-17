from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# Create your tests here.
#
class ApiDeleteExamWithGrade(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="quimpm",
            password="testingquimpm123",
            email="quimpm@gmail.com",
            first_name="Quim",
            last_name="També",
        )

    def test_get_user(self):
        response = self.client.get("/user/1/")
        expected = {"id": 1, "username": "quimpm", "email": "quimpm@gmail.com"}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.data)

    def test_not_found(self):
        response = self.client.get("/user/2/")
        self.assertEqual(404, response.status_code)
