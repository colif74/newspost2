from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Подсказка вашей команды'
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True
    # напоминать ли о миграциях. Если true — то будет
    # напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        # здесь можете писать любой код,
        # который выполняется при вызове вашей команды
        self.stdout.write(str(options['argument']))