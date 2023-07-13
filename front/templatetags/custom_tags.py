from django import template

register = template.Library()

@register.filter(name='floatmul')
def floatmul(value, arg):
    return float(value) * float(arg)


@register.filter(name='floatadd')
def floatadd(value, arg):
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0.0
    