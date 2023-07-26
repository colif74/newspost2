from django.core.management.base import BaseCommand, CommandError
from NewsPaper.news.models import *


class Command(BaseCommand):
    help = 'Подсказка вашей команды'
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True
    # напоминать ли о миграциях.
    # Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Вы действительно хотите удалить все новости этой категории? yes/no')
        # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Все новости этой категории удалены!'))
            return

        self.stdout.write(
            self.style.ERROR('Недоступно'))
        # в случае неправильного подтверждения, говорим, что в доступе отказано
