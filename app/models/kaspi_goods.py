from django.db import models


class KaspiGoodsModel(models.Model):

    sku = models.CharField(max_length=256, null=False)
    model = models.CharField(max_length=256, null=False)
    competitors_prices = models.JSONField(verbose_name='Цены конкурентов')
    current_price = models.IntegerField(verbose_name='Актуальная цена')
    min_price = models.IntegerField(verbose_name='Минимальная цена')
    price_step = models.IntegerField(verbose_name='Шаг цены')

    def __str__(self):
        return f"sku: {self.sku} model: {self.model}"

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "kaspi_goods"
