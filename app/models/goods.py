from django.db import models

from app.models.competitor_goods import CompetitorGoodsModel


class GoodsModel(models.Model):
    objects = models.Manager()  # Add the default manager

    store_good_id = models.IntegerField(null=False, unique=True, verbose_name='Id продукта из магазина')
    name = models.CharField(max_length=256, unique=True, verbose_name='Название')
    code = models.CharField(max_length=256, unique=True, verbose_name='Код')
    minimal_price = models.IntegerField(null=False, verbose_name='Минимальная цена')

    competitor_goods = models.ManyToManyField(
        CompetitorGoodsModel, related_name='goods', verbose_name='Товары конкурентов'
    )

    def __str__(self):
        return self.name

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "goods"
