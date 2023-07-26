from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_rating_post = Post.objects.filter(author_id=self.pk).\
            aggregate(post_rating_sum=Coalesce(Sum('rating_post') * 3, 0))
        author_rating_comment = Comment.objects.filter(user_id=self.user).\
            aggregate(comment_rating_sum=Coalesce(Sum('rating_comment'), 0))
        author_rating_comment_post = Comment.objects.filter(post__author__id=self.user).\
            aggregate(post_comment_rating_sum=Coalesce
        (Sum('rating_comment'), 0))
        self.rating = author_rating_post['post_rating_sum'] + author_rating_comment['comment_rating_sum'] \
            + author_rating_comment_post['post_comment_rating_sum']
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'authors-{self.pk}')


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=20, default='местные новости', help_text='category name')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='subscribers')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    objects = None
    news = 'NW'
    states = 'PS'

    TYPE = [
        (news, 'Новость'),
        (states, 'Статья')
    ]

    post_tip = models.CharField(max_length=10, choices=TYPE, default=states)
    date_in = models.DateField(auto_now_add=True)
    header = models.CharField(max_length=255)
    contents = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category, through='PostCategory', related_name='PostCategory')
    rating_post = models.IntegerField(default=0, validators=[MinValueValidator(0.0)])

    def likes(self):
        self.rating_post += 1
        self.save()

    def dislikes(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f"{self.contents[:124]}..."

    def __str__(self):
        return f'{self.header.title()}:{self.contents[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'posts-{self.pk}')
        # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    text_comment = models.TextField(blank=True)
    date_in = models.DateField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
