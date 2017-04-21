from django.test import TestCase
from django.test import Client

# Create your tests here.

class SimpleSiteTests(TestCase):
    
    def setUp(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
    
    def test_assertion(self):
        self.assertTrue(True)

    def test_index_page(self):
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        