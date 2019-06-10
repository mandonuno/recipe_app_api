from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Tests when creating a user w/ an email is sucessfull"""
        email = 'test@vestthedev.com'
        password = 'tuna123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normal(self):
        """Test for new user is normalized"""
        email = 'test@VESTTHEDEV.COM'
        user = get_user_model().objects.create_user(email, 'tuna123')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Tests raises error when creating user with no email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'tuna123')
    
    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@VESTTHEDEV.COM',
            'tuna123'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)