from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_attr')
def add_attr(field, attr_string):
    if not isinstance(field, BoundField):
        return field 

    attrs = {}
    for attr in attr_string.split(","):
        key, value = attr.split(":")
        attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)


@register.filter
def multiply(value, arg):
    return value * arg