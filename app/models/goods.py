from django.db import models

from app.models.competitor_goods import CompetitorGoodsModel


class GoodsModel(models.Model):
    objects = models.Manager()  # Add the default manager

    store_good_id = models.IntegerField(null=False, unique=True, verbose_name='Id продукта из магазина')
    name = models.CharField(max_length=256, unique=True, verbose_name='Название')
    code = models.CharField(max_length=256, unique=True, verbose_name='Код')
    minimal_price = models.IntegerField(verbose_name='Минимальная цена')
    current_price = models.IntegerField(verbose_name='Актуальная цена')
    updated_at = models.DateTimeField(verbose_name='Обновлено в', auto_now=True)

    competitor_goods = models.ManyToManyField(
        CompetitorGoodsModel,
        related_name='goods',
        verbose_name='Товары конкурентов',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        # Указывает имя таблицы в базе данных
        db_table = "goods"
