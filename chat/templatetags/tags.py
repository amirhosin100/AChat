from django import template

register = template.Library()

EN_TO_FA = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

@register.filter(name="fa")
def to_persian_numbers(value):
    return ''.join(EN_TO_FA.get(ch, ch) for ch in str(value))