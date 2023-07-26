from .models import Category, Post, Author
from modeltranslation.translator import register, \
    TranslationOptions
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

# @register(Category)
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('name', 'subscribers',)
    # указываем, какие именно поля надо переводить в виде кортежа


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('user',)

@register(Post)
class PostranslationOptions(TranslationOptions):
    fields = ('post_tip', 'header', 'contents',)

