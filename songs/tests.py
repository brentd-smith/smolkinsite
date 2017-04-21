from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup

# Create your tests here.

class SimpleSiteTests(TestCase):

    def test_assertion(self):
        self.assertTrue(True)

    def test_index_page(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('')
        self.assertEqual(r.status_code, 200)



