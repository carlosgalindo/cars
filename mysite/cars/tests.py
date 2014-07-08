from django.test import TestCase

from cars.models import *

# Pending to create sufficient test cases.
# Temporary test database, not affecting production.

class CarMethodTests(TestCase):

    def test_pending(self):
        car = Car()
        self.assertEqual(car.test_value(), True)
