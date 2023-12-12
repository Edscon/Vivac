from django import template

register = template.Library()

@register.filter
def replace_1(value):
    return value.replace("|","/")

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def suma(value, arg):
    value = float(value)
    return value + arg

@register.filter
def resta(value, arg):
    value = float(value)
    return value - arg

