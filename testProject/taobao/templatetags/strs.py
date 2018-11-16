from django import template
register = template.Library()



@register.simple_tag
def replace_str(v):
    return '/static/'+str(v)