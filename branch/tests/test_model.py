from django.test import TestCase
from country.models import Country
from .models import Branch

class BranchModelTestCase(TestCase):
    def setUp(self):
        # Create a Country instance for testing
        self.country = Country.objects.create(name='Test Country')

        # Create a Branch instance for testing
        self.branch_data = {
            'name': 'Test Branch',
            'country': self.country,
            'city': 'Test City',
            'mobile': '1234567890',
            'telephone': '9876543210',
            'cr': 'CR123456',
            'email': 'test.branch@example.com',
            'website': 'http://www.testbranch.com',
            'logo': 'path/to/test/logo.png',
        }
        self.branch = Branch.objects.create(**self.branch_data)

    def test_branch_model_fields(self):
        # Retrieve the model instance created in setUp
        test_branch = Branch.objects.get(name='Test Branch')

        # Perform assertions to test model fields
        self.assertEqual(test_branch.name, 'Test Branch')
        self.assertEqual(test_branch.country, self.country)
        self.assertEqual(test_branch.city, 'Test City')
        self.assertEqual(test_branch.mobile, '1234567890')
        self.assertEqual(test_branch.telephone, '9876543210')
        self.assertEqual(test_branch.cr, 'CR123456')
        self.assertEqual(test_branch.email, 'test.branch@example.com')
        self.assertEqual(test_branch.website, 'http://www.testbranch.com')
        self.assertEqual(test_branch.logo, 'path/to/test/logo.png')

    def test_branch_model_str_representation(self):
        # Test the __str__ method of the model
        self.assertEqual(str(self.branch), 'Test Branch')

    def test_branch_model_unique_email(self):
        # Test uniqueness constraint on email field
        duplicate_branch = Branch(**self.branch_data)
        with self.assertRaises(Exception):
            duplicate_branch.save()

    # Add more test methods as needed
