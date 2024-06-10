from django.db import models


class CompetitorGoodsModel(models.Model):
    url = models.URLField(verbose_name='Ссылка на карточку товара', null=False)
