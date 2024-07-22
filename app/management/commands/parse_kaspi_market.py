import openpyxl
from django.core.management.base import BaseCommand

from app.models import KaspiGoodsModel


class Command(BaseCommand):
    help = 'Спарсить цены с каспи на товары'

    def handle(self, *args, **kwargs):
        all_goods: list[KaspiGoodsModel] = KaspiGoodsModel.objects.all()
        for good in all_goods:
            if "_Ledvisionkz" in good.sku:
                goods_sku = good.sku.split("_")[0]
                print(goods_sku)
        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно!'))
