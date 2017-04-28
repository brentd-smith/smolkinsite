from django import template
import datetime

register = template.Library()

@register.simple_tag(name='URL_PREFIX')
def get_url_prefex():
    # return "https://ian-smolkin-synagogue-audio.s3.amazonaws.com/"
    return "http://ian-smolkin-synagogue-audio.s3-website-us-east-1.amazonaws.com/"

@register.simple_tag(name='CURRENT_YEAR')
def current_year():
    return datetime.date.today().year

@register.simple_tag(name="TORAH")
def torah_reading_path():
    return "TorahReading"

@register.simple_tag(name="HAFTARAH")
def haftarah_reading_path():
    return "HaftarahReading"

@register.simple_tag(name="SERVICE")
def service_path():
    return "ServiceName"