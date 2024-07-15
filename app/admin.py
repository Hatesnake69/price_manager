from django.contrib import admin
from django.utils.html import format_html

from app.models import GoodsModel, CompetitorGoodsModel, KaspiGoodsModel


class CompetitorGoodsInline(admin.TabularInline):
    model = GoodsModel.competitor_goods.through
    extra = 1


@admin.register(KaspiGoodsModel)
class KaspiGoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "model",
        "competitors_prices",
        "current_price",
        "min_price",
        "price_step",
    )


@admin.register(GoodsModel)
class GoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "price_step",
        "minimal_price",
        "current_price",
        "competitor_goods_list"
    )
    exclude = ("competitor_goods", )
    inlines = [CompetitorGoodsInline]

    def competitor_goods_list(self, obj):
        competitors = obj.competitor_goods.all()
        return format_html('<br>'.join([f'{competitor}' for competitor in competitors]))
    competitor_goods_list.short_description = 'Товары конкурентов'


@admin.register(CompetitorGoodsModel)
class CompetitorGoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "current_price",
    )
