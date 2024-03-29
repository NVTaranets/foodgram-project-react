import csv
import os

from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredients

from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Import initial data from file data/*.csv args sequensial'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        obj = {
            'ingredients.csv': Ingredients
        }
        name_fields = {
            'ingredients.csv': ('name', 'measurement_unit')
        }
        for file_csv in options['files']:
            if file_csv not in obj.keys():
                raise CommandError('Unknown file to import "%s"' % file_csv)
            try:
                full_fn = os.path.join(BASE_DIR, file_csv)
                with open(full_fn, 'r', newline='', encoding='utf-8') as csvf:
                    reader = csv.reader(csvf)
                    list_obj = list()
                    for row in reader:
                        kwargs = dict(zip(name_fields[file_csv], row))
                        list_obj.append(obj[file_csv](**kwargs))
                    obj[file_csv].objects.bulk_create(list_obj)
            except OSError:
                raise CommandError('File "%s" does not exist' % file_csv)
            self.stdout.write(
                self.style.SUCCESS('Successfully files "%s"' % file_csv)
            )
