from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup

# Create your tests here.

class SimpleSiteTests(TestCase):
    
    c = Client()
    
    def setUp(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
    
    def test_assertion(self):
        self.assertTrue(True)

    def test_index_page(self):
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        obj = BeautifulSoup(response.content, "html.parser")

        