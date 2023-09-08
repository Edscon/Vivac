from django import template

register = template.Library()

@register.filter
def replace_1(value):
    return value.replace("|","/")

@register.filter
def multiply(value, arg):
    return value * arg