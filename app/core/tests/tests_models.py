from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def test_user(email='test@elguerodev.com', password='test123'):
    """Create a test user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Tests when creating a user w/ an email is sucessfull"""
        email = 'test@vestthedev.com'
        password = 'tuna123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
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

    def test_tag_str(self):
        """Test the tag string"""
        tag = models.Tag.objects.create(
            user=test_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=test_user(),
            name='Carrot'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=test_user(),
            title='Chicken curry',
            time_minutes=15,
            price=10.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is save in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, expected_path)
