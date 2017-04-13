from django import template

register = template.Library()

@register.simple_tag(name='URL_PREFIX')
def get_url_prefex():
    # return "https://ian-smolkin-synagogue-audio.s3.amazonaws.com/"
    return "http://ian-smolkin-synagogue-audio.s3-website-us-east-1.amazonaws.com/"
