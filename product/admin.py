from django.contrib import admin
from . import models

# Register your models here.


class InlineVariation(admin.TabularInline):
    model = models.Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'formatted_price', 'formatted_marketing_price']
    inlines = [
        InlineVariation
    ]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation)
