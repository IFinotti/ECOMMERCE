from django.contrib import admin
from .forms import VariacaoObrigatoria
from . import models


class VariationInline(admin.TabularInline):
    model = models.Variation
    formset = VariacaoObrigatoria
    min_num = 1
    extra = 0
    can_delete = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortest_description',
                    'get_formatted_price', 'get_formatted_promotional_price']
    inlines = [
        VariationInline
    ]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation)
