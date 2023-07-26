from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    # author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор', empty_label='Любой')
    # header = ModelChoiceFilter(field_name='header', queryset= Post.objects.all(), label='Заголовок', empty_label='Любой')
    # date_in = ModelChoiceFilter(field_name='date_in', queryset=Post.objects.all(), label='Дата публикации', empty_label='Любая')

    class Meta:
        model = Post
        fields = {
           'header': ['iexact'],
           'author': ['exact'],
           'date_in': ['iexact'],
            }
