from django.contrib import admin
from .models import Author, Post, Category, Appointment
from modeltranslation.admin import TranslationAdmin
# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class PostTrans(TranslationAdmin):
    model = Post


class AuthorTrans(TranslationAdmin):
    model = Author

#
# def nullfy_rating(queryset):
#     queryset.update(rating=0)
#
#     nullfy_rating.short_description = 'Обнулить товары'
# # описание для более понятного представления в админ панеле задаётся,
# # как будто это объект
#
#
# # создаём новый класс для представления товаров в админке
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('post_tip', 'header', 'date_in', 'author')
#     # оставляем только имя и цену товара
#     list_filter = ('author', 'header', 'post_tip')
#     # добавляем примитивные фильтры в нашу админку
#     search_fields = ('header', 'category__name')
#     # тут всё очень похоже на фильтры из запросов в базу
#
#
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'rating')
#     # оставляем только имя и цену товара
#     list_filter = ('user', 'rating')
#     # добавляем примитивные фильтры в нашу админку
#
#
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



admin.site.register(Author, AuthorTrans)
admin.site.register(Post, PostTrans)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Appointment)

# Register your models here.
