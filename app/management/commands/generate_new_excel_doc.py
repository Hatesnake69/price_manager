import io

import openpyxl
from django.core.management.base import BaseCommand

from app.models import KaspiGoodsModel
from app.utils.send_docs_via_tg import send_docs


class Command(BaseCommand):
    help = 'Создаёт документ с обновленными ценами'

    def handle(self, *args, **kwargs):
        output = io.BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'KaspiGoods'

        # Запись заголовков столбцов
        sheet.append([
            "sku",
            "model",
            "brand",
            "price",
            "pp1",
            "pp2",
            "pp3",
            "pp4",
            "pp5",
            "preorder",
        ])
        for good in KaspiGoodsModel.objects.order_by('id'):
            sheet.append([
                good.sku,
                good.model,
                good.brand,
                good.price,
                good.pp1,
                good.pp2,
                good.pp3,
                good.pp4,
                good.pp5,
                good.preorder,
            ])
        workbook.save(output)
        output.seek(0)
        send_docs(docs=[output])
        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))

