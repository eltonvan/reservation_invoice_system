from django import template

register = template.Library()

@register.filter
def percentage(value, arg=1):
    try:
        float_value = float(value)
        return f"{float_value:.{arg}f}%"
    except (ValueError, TypeError):
        return value 
