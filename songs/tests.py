from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup
import re

import text2service

# Create your tests here.

class SimpleSiteTests(TestCase):
    
    def setUp(self):
        text2service.addServices()

    # testing suite is working as expected
    def test_assertion(self):
        self.assertTrue(True)

    # expected index page is present with expected table header text
    def test_index_page(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        expected = "<th>Learning the Services</th>"
        self.assertEqual(str(obj.th), expected)

    # all expected services are present
    def test_index_page_services(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        services = obj.findAll("td")
        self.assertEqual(len(services), 6)
        
        serv = ['Kabbalat Shabbat', 'Friday Night Maariv', 'Shabbat Torah Service', 'Shabbat Musaf Service', 'Torah Reading', 'Haftarah Readings']
        for s in serv:
            # searchPattern = '<td><a href="/ServiceName/{}/">{}</a></td>'.format(s, s)
            # self.assertTrue(searchPattern in services, "Did not find {} in {}".format(searchPattern, services))
            self.assertTrue(re.search(s, str(obj)))



