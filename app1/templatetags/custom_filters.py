import base64
from django import template

register = template.Library()

@register.filter
def base64_encode(value):
    encoded_data = base64.b64encode(value).decode('utf-8')
    return encoded_data
