from django import template


register = template.Library()

@register.filter()
def post_author():
    return Post.objects.get(author_id= contents)
