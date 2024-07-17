from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class MyModelViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.users_base_url = '/users/'
        self.valid_data = {"username": "Anakin",
                           "email": "vader@deathstar.com"}
        self.invalid_data = {"foo": "bar"}

    def test_list(self):
        response = self.client.get(self.users_base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        user_instance = User.objects.create(
            username="Anakin",
            email="vader@deathstar.com"
        )
        response = self.client.get(f"/users/{user_instance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "Anakin")

    def test_create(self):
        response = self.client.post(self.users_base_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid(self):
        response = self.client.post(self.users_base_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        user_instance = User.objects.create(
            username="Vader",
            email="vader@deathstar.com"
        )
        response = self.client.put(
            f'/users/{user_instance.id}/', self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'Anakin')

    def test_partial_update(self):
        user_instance = User.objects.create(
            username="Vader",
            email="vader@deathstar.com"
        )
        response = self.client.patch(
            f'/users/{user_instance.id}/', {"username": "darthvader"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "darthvader")

    def test_delete(self):
        user_instance = User.objects.create(
            username="Vader",
            email="vader@deathstar.com"
        )
        response = self.client.delete(f'/users/{user_instance.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
