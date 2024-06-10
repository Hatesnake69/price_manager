from django.contrib import admin

# Register your models here.
from app.models import GoodsModel, CompetitorGoodsModel


@admin.register(GoodsModel)
class GoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "minimal_price",
    )


@admin.register(CompetitorGoodsModel)
class CompetitorGoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "url",
    )
