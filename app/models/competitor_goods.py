from django.db import models


class CompetitorGoodsModel(models.Model):

    url = models.URLField(verbose_name='Ссылка на карточку товара', null=False)
    price_xpath = models.CharField(max_length=256, verbose_name='Xpath цены', null=False)
    current_price = models.IntegerField(verbose_name='Актуальная цена')

    def __str__(self):
        return f"цена: {self.current_price}, ссылка: {self.url}"

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "competitor_goods"
