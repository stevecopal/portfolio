from django import template

register = template.Library()

@register.filter
def get_model_name(obj):
    return obj._meta.model_name