from django.db import models


class KaspiGoodsModel(models.Model):
    objects = models.Manager()

    sku = models.CharField(max_length=256, null=False)
    model = models.CharField(max_length=256, null=False)
    brand = models.CharField(max_length=256, null=False)
    price = models.IntegerField()
    pp1 = models.CharField(max_length=256, null=True)
    pp2 = models.CharField(max_length=256, null=True)
    pp3 = models.CharField(max_length=256, null=True)
    pp4 = models.CharField(max_length=256, null=True)
    pp5 = models.CharField(max_length=256, null=True)
    preorder = models.CharField(max_length=256, null=True)
    competitors_prices = models.JSONField(verbose_name='Цены конкурентов', null=True)
    min_price = models.IntegerField(verbose_name='Минимальная цена')
    price_step = models.IntegerField(verbose_name='Шаг цены')
    kaspi_offer_url = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"sku: {self.sku} model: {self.model}"

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "kaspi_goods"
