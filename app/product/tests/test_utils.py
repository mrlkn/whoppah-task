from django.contrib.auth.models import User
from django.test import TestCase
from product.utils import is_valid_transition


class IsValidTransitionTest(TestCase):

    def setUp(self):
        self.admin_user = User(is_staff=True)
        self.creator_user = User()

        self.product_instance = type('Product', (object,), {'state': 'draft', 'created_by': self.creator_user})

    def test_is_valid_transition(self):
        """
        Test the is_valid_transition function
        """

        is_valid = is_valid_transition(self.product_instance, 'new', self.creator_user)
        self.assertTrue(is_valid)

        self.product_instance.state = 'new'
        is_valid = is_valid_transition(self.product_instance, 'accepted', self.admin_user)
        self.assertTrue(is_valid)

        is_valid = is_valid_transition(self.product_instance, 'new', self.admin_user)
        self.assertFalse(is_valid)

    def test_is_valid_transition_for_creator(self):
        """
        Test the is_valid_transition function for a creator user
        """

        is_valid = is_valid_transition(self.product_instance, 'new', self.creator_user)
        self.assertTrue(is_valid)

        self.product_instance.state = 'new'
        is_valid = is_valid_transition(self.product_instance, 'accepted', self.creator_user)
        self.assertFalse(is_valid)

    def test_is_valid_transition_for_admin(self):
        """
        Test the is_valid_transition function for an admin user
        """

        self.product_instance.state = 'new'
        is_valid = is_valid_transition(self.product_instance, 'accepted', self.admin_user)
        self.assertTrue(is_valid)

        is_valid = is_valid_transition(self.product_instance, 'new', self.admin_user)
        self.assertFalse(is_valid)

    def test_is_valid_transition_with_invalid_state(self):
        """
        Test the is_valid_transition function with an invalid state
        """

        is_valid = is_valid_transition(self.product_instance, 'invalid_state', self.admin_user)
        self.assertFalse(is_valid)

