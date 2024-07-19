from django.contrib import admin
from django.utils.html import format_html

from app.models import KaspiGoodsModel


@admin.register(KaspiGoodsModel)
class KaspiGoodsModelAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "model",
        "price",
        "min_price",
        "price_step",
        "competitors_prices",
    )
