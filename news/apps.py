from django.apps import AppConfig
import redis

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

   # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        from .signals import send_notifications, notify_about_new_post

red = redis.Redis(
    host='redis-10946.c284.us-east1-2.gce.cloud.redislabs.com',
    port=10946,
    password='ttSVozCYqxUDd2qNBLxFFHK0CYOedYHS'

)