import openpyxl
from django.core.management.base import BaseCommand

from app.models import KaspiGoodsModel


class Command(BaseCommand):
    help = 'Загружает товары из экселя в модели каспи товаров'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        # Логика твоей команды
        # Открываем файл
        workbook = openpyxl.load_workbook(kwargs['file_path'])
        # Получаем первый лист
        sheet = workbook.active

        # Проходим по строкам и столбцам листа

        goods = []
        pass_1st = True
        for row in sheet.iter_rows(values_only=True):
            if pass_1st:
                pass_1st = False
                continue
            try:
                good = {
                    "sku": row[0],
                    "model": row[1],
                    "brand": row[2],
                    "price": row[3],
                    "pp1": row[4],
                    "pp2": row[5],
                    "pp3": row[6],
                    "pp4": row[7],
                    "pp5": row[7],
                    "preorder": row[8],
                    "min_price": round(row[3] * 7/10),
                    "price_step": 0,
                }
                KaspiGoodsModel.objects.create(
                    **good
                )
            except:
                print("error occurred")
        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
