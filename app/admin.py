from django.contrib import admin

# Register your models here.
from app.models import GoodsModel, CompetitorGoodsModel


class CompetitorGoodsInline(admin.TabularInline):
    model = GoodsModel.competitor_goods.through
    extra = 1


@admin.register(GoodsModel)
class GoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "minimal_price",
    )
    exclude = ("competitor_goods", )
    inlines = [CompetitorGoodsInline]


@admin.register(CompetitorGoodsModel)
class CompetitorGoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "url",
    )
