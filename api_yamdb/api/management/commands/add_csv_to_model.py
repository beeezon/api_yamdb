import csv
import os
import io
from django.apps import apps
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def get_csv_file(self, filename):
        path = os.path.join("data", filename)
        file_path = finders.find(path)
        return file_path

    def add_arguments(self, parser):
        parser.add_argument("direction", type=str, help="Укажите имя файла файла")
        parser.add_argument('model_name', type=str, help="Укажите имя модели")
        parser.add_argument('app_name', type=str, help="Укажите имя прилжоения")


    def handle(self, *args, **options):
        direction = options["direction"]
        file_path = self.get_csv_file(direction) # Путь до файла
        _model = apps.get_model(options['app_name'], options['model_name']) # Получил модель
        with io.open(file_path, encoding='utf-8') as csv_file:
            data = csv.reader(csv_file, delimiter=',', quotechar='|')
            header = next(data)
            for row in data:
                _object_dict = {key: value for key, value in zip(header, row)}
                _model.objects.get_or_create(**_object_dict)
                self.stdout.write(self.style.SUCCESS(
                    f"Загрузка данных из {options['direction']} в модель {options['model_name']} произведена успешно"
                ))

