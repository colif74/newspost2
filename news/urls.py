from django.urls import path, include
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import LoginView, LogoutView
from .views import PostList, AuthorList, PostDetail, \
    IndexView, BaseRegisterView, CategoryList, AuthorDetail, PostCategory, \
    PostCreateView, PostDeleteView, PostUpdateView, ArticleCreate, \
    AppointmentView, unsubscribe, subscribe, upgrade_me

urlpatterns = [path('', IndexView.as_view()),
               path('upgrade/', upgrade_me, name='upgrade'),
               path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
               path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
               path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
               path('news/', PostList.as_view(), name='posts-list'),
               path('author/', AuthorList.as_view(), name='authors'),
               path('author/<int:pk>', AuthorDetail.as_view(), name='author'),
               path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
               path('news/create/', PostCreateView.as_view(), name='`post_create`'),
               path('article/create/', ArticleCreate.as_view(), name='article_create'),
               path('news/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
               path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
               path('category/', CategoryList.as_view(), name='categories'),
               path('category/<int:pk>', PostCategory.as_view(), name='posts_of_category_list'),
               path('category/<int:pk>/subscribers', subscribe, name='subscribers'),
               path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
               path('accounts/', include('allauth.urls')),
               path('appointment/', AppointmentView.as_view(), name='make_appointment'),
               ]
