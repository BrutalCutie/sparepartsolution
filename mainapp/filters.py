from django import template

register = template.Library()


@register.filter
def readed_messages(value, arg):
    # return [x for x in value if x.readed == arg]
    return value * arg
