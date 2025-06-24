from django import template

register = template.Library()


@register.filter(name="unique_count")
def unique_count(value):
    """Фильтр для подсчета уникальных значений в списке"""
    return len(set(value))
