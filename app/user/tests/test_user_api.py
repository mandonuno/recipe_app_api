from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

    def test_create_user_token(self):
        """Test token is created for the user"""
        user_token = {'email': 'test@elguerodev.com', 'password': 'test123'}
        create_user(**user_token)

        res = self.client.post(TOKEN_URL, user_token)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        """Test token has invalid data"""
        create_user(email='test@elgureodev.com', password='test123')

        user_token = {'email': 'test@elguerodev.cm', 'password': 'badpass'}

        res = self.client.post(TOKEN_URL, user_token)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_no_user(self):
        """Test token not created for invalid user"""
        user_token = {'email': 'test@elguerodev.com', 'password': 'test123'}

        res = self.client.post(TOKEN_URL, user_token)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_fields(self):
        """Test that email and password are required fields"""
        res = self.client.post(TOKEN_URL, {'email': 'dev', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorize_user(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Tests Api requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@elguerodev.com',
            password='test123',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving successfull logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_fail(self):
        """Test post is not allowed on ME URL"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test for updating user profile for authenticated user"""
        user_http = {'name': 'new name', 'password': 'newpass123'}

        res = self.client.patch(ME_URL, user_http)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, user_http['name'])
        self.assertTrue(self.user.check_password(user_http['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
