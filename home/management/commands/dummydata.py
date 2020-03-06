from django.core.management.base import BaseCommand, CommandError

from . import _provider


class Command(BaseCommand):

    help = '더미 데이터 생성기'

    def add_arguments(self, parser):
        parser.add_argument('cnt', nargs=1, type=int)

    def handle(self, *args, **options):
        try:
            cnt = int(options['cnt'][0])
        except ValueError:
            raise CommandError('Not integer!')

        if cnt <= 0:
            raise CommandError('greater than or equal to 1.')

        for i in range(cnt):
            _provider.AccountFactory()
