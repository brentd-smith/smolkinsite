from django.test import TestCase
from django.test import Client
from bs4 import BeautifulSoup
import re

import text2service
import text2torah

from django.core.management import call_command
from django.utils.six import StringIO

# ------------------------------------------------------------------------------
# Test of the Index page, and the Services pages
# ------------------------------------------------------------------------------
class SimpleSiteTests(TestCase):
    
    def setUp(self):
        text2service.loadTestData()

    # Make sure the testing suite is working as expected.
    def test_assertion(self):
        self.assertTrue(True)

    # Make sure the index page is present with the expected table header text.
    def test_index_page(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        expected = "<th>Learning the Services</th>"
        self.assertEqual(str(obj.th), expected)

    # Make sure the index page returns correctly and that all expected services are present.
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


    # Make sure the song_list page returns correctly.
    def test_service_song_list(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('/ServiceName/KabbalatShabbat/')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        expected = "<th>Songs for Kabbalat Shabbat</th>"
        self.assertEqual(str(obj.th), expected)

        obj = BeautifulSoup(r.content, "html.parser")
        first  = obj.find("td")
        self.assertTrue(re.search("Shalom Alechem", str(first)))
        
    # Make sure the song_detail page returns correctly.
    def test_service_song_detail(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('/ServiceName/KabbalatShabbat/ShalomAlechem/')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        expected = "<h3>Shalom Alechem</h3>"
        self.assertEqual(str(obj.h3), expected)

        obj = BeautifulSoup(r.content, "html.parser")
        first  = obj.find("h4")
        self.assertTrue(re.search("Shalom Alechem A.mp3", str(first)))

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
class Text2TorahTests(TestCase):
    
    # TODO: Create a loadTestData procedure that loads a limited set of data for testing purposes
    # that will help keep the tests fast...
    def setUp(self):
        text2torah.loadTestData()

    def test_get_object_key(self):
        # filename: 3rd Triennial Noach 6th Aliyah.pdf
        # returns:  07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/
        result = text2torah.get_object_key("3rd Triennial Noach 6th Aliyah.pdf", debug=False)
        self.assertEqual(result, "07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah")

    def test_book_list(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('/TorahReading/')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        title = obj.th
        self.assertEqual(str(title), "<th>Books In The Torah</th>")
        
    def test_parsha_list(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('/TorahReading/Breshit/')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        title = obj.th
        self.assertEqual(str(title), "<th>Parshas in Breshit (Genesis)</th>")

        # should have a list of Parshas, starting with Breshit    
        first = obj.find("td")
        self.assertTrue(re.search("Breshit", str(first)))

    def test_torah_reading_list(self):
        # "<th>Torah Readings in {{ parsha.display }}</th>"
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = c.get('/TorahReading/Breshit/Breshit/')
        self.assertEqual(r.status_code, 200)
        
        obj = BeautifulSoup(r.content, "html.parser")
        title = obj.th
        self.assertEqual(str(title), "<th>Torah Readings in Parshat Breshit</th>")

        # should have a list of Parshas, starting with Breshit    
        first = obj.find("td")
        self.assertTrue(re.search("2nd Triennial 5th Aliyah", str(first)))

# ------------------------------------------------------------------------------
# Management Command Tests
# ------------------------------------------------------------------------------
class ManagementCommandTests(TestCase):
    
    def test_hello(self):
        out = StringIO()
        call_command('hello', 51, stdout=out)
        self.assertIn('Hello id=51', out.getvalue())

import smolkinsite.settings
# ------------------------------------------------------------------------------
# Configuration Tests
# ------------------------------------------------------------------------------
class ConfigurationTests(TestCase):
    
    def setUp(self):
        pass

    def test_cookie_settings(self):
        self.assertTrue(smolkinsite.settings.CSRF_COOKIE_SECURE != smolkinsite.settings.DEBUG)
        self.assertTrue(smolkinsite.settings.SESSION_COOKIE_SECURE != smolkinsite.settings.DEBUG)
    
    def test_allowed_hosts(self):
        if smolkinsite.settings.DEBUG:
            self.assertIn('*', smolkinsite.settings.ALLOWED_HOSTS)
        else:
            self.assertNotIn('*', smolkinsite.settings.ALLOWED_HOSTS)
    
    