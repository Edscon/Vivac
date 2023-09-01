from django import template

register = template.Library()

@register.filter
def replace_1(value):
    return value.replace("|","/")