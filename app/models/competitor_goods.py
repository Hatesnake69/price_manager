from django.db import models


class CompetitorGoodsModel(models.Model):

    url = models.URLField(verbose_name='Ссылка на карточку товара', null=False)
    price_xpath = models.CharField(max_length=256, verbose_name='Xpath цены', null=False)

    def __str__(self):
        return self.url
