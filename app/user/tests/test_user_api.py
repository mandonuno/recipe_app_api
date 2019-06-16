from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the users API"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid(self):
        """Test creating user is successfull"""
        user_http = {
            'email': 'test@elguerodev.com',
            'password': 'test123',
            'name': 'guero'
        }
        res = self.client.post(CREATE_USER_URL, user_http)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(user_http['password']))

    def test_user_exists(self):
        """Test created user already exitsts"""
        user_http = {'email': 'test@elguerodev.com', 'password': 'test123'}

        create_user(**user_http)

        res = self.client.post(CREATE_USER_URL, user_http)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        """Test created user password less than 6 characters"""
        user_http = {'email': 'test@elguerodev.com', 'password': 'pw'}

        res = self.client.post(CREATE_USER_URL, user_http)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=user_http['email']
        ).exists()

        self.assertFalse(user_exists)
