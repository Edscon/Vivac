from django import template
from datetime import datetime
from googletrans import Translator

register = template.Library()

@register.filter
def replace_1(value):
    return value.replace("|","/")

def replace_2(value):
    return value.replace("/","|")

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

@register.filter
def date1(value):
    value = datetime.strptime(str(value).split(" ")[0], '%Y-%m-%d').date()
    return value

@register.filter
def lower_(value):
    return str(value).lower()

translator = Translator()
@register.filter
def trans_ca(value):
    return translator.translate(value, dest='ca').text