from django import template

register = template.Library()

# Allow changes to variables in templates
@register.simple_tag
def update_variable(value):
    return value


# templatetags (must be spelled that way) needs to be in the same level as models.py and views.py
# That's why it's here
