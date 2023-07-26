from django import template


register = template.Library()

CENSOR_TABLE = {
    'редиска': 'р.....',
}


@register.filter()
def censor(value, code='text'):
    postfix = CENSOR_TABLE[code]
    return f'{value} {postfix}'
