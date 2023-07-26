import pytz
from django.views.generic import ListView, DetailView, CreateView,\
    TemplateView, UpdateView, DeleteView
from .models import Post, Author, Category, Appointment
from .filters import PostFilter
from datetime import datetime
from django.views import View
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail
from django.template.loader import render_to_string
from .forms import PostForm,  BaseRegisterForm
from .tasks import send_email_post
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.decorators import login_required
import logging
# from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.utils import timezone


class NewsTime(View):
    def get(self, request):
        local_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
            'local_time': timezone.now(),
            'timezones': pytz.common_timezones
            # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'news.html', context))

        #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware

    def pst(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostTrans(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'news.html', context))


class AuthorTrans(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Author.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'authors.html', context))


class CategoryTrans(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Category.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'categories.html', context))


logger = logging.getLogger(__name__)

@pgettext_lazy
def get(self, request):
    string = Post.objects.get('id')
    return HttpResponse(string)


def some_view(request):
    if logger:
        logger.warning('Platform is running at risk')


class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry()
        return super().form_valid(form)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'signup.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'endex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class AuthorList(ListView):
    model = Author
    ordering = '-user'
    template_name = 'author/authors.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Author.objects.get(pk=self.kwargs['pk']).post_set.all().order_by('-id')
        return context


class PostList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'post/news.html'
    context_object_name = 'posts'
    paginate_by = 15

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'posts'


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('news/')

    return render(request, 'post/post_edit.html', {'form': form})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    permission_required = ('news.update_post',)
    form_class = PostForm
    success_url = '/news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_tip = 'NW'
        return super().form_valid(form)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_update.html'
    permission_required = ('news.create_post',)
    form_class = PostForm
    success_url = '/news'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_tip = 'NW'
        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    permission_required = ('post.post_delete',)
    form_class = PostForm
    success_url = '/news'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('post.add_post')
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_title = 'ST'
        post.save()
        send_email_post.delay(post.pk)
        return super().form_valid(form)


class CategoryList(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'


class PostCategory(ListView):
    model = Post
    ordering = '-id'
    template_name = 'post/news.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.queryset = Category.objects.get(pk=self.kwargs['pk']).PostCategory.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in Category.objects.get(pk=self.kwargs['pk']).\
            subscribers.all()
        context['category'] = self.queryset
        return context


class AppointmentView(View):
    def bick(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def bick_post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='colif74@yandex.ru',
            to=['colif@mail.ru', 'colif74@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
        send_mail(
                    subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
                    # имя клиента и дата записи будут в теме для удобства
                    message=appointment.message,  # сообщение с кратким описанием проблемы
                    from_email='colif74@yandex.ru',
                    # здесь указываете почту, с которой будете отправлять (об этом попозже)
                    recipient_list=['colif@mail.ru', 'colif74@gmail.com']
                    # здесь список получателей. Например, секретарь, сам врач и т. д.
                )

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('news:make_appointment')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы в рассылке категории"
    return render(request, 'subscribers.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от рассылки: '
    return render(request, 'subscribers.html', {'category': category, 'message': message})


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        return redirect('/')
