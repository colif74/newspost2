from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .models import Post, Category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


class PostForm(forms.ModelForm):
    header = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = [
                'post_tip',
                'category',
                'header',
                'contents',
                'author',
                    ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get('header')
        contents = cleaned_data.get("contents")
        if contents == header:
            raise ValidationError({"Содержание должно отлтчатся от заголовка"})
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


# @login_required
# def upgrade_me(request):
#     user = request.user
#     author_group = Group.objects.get(name='author')
#     if not request.user.groups.filter(name='author').exists():
#         author_group.user_set.add(user)
#         return redirect('/')

# `
# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     message = "Вы в рассылке категории"
#     return render(request, 'category/subscribers.html', {'category': category, 'message': message})`
