from django import template
register = template.Library()


@register.filter
def addclasses(value, arg):
    return value.as_widget(attrs={'class': arg})
