from django.contrib import admin
from . import models


# Define an inline admin class for OrderItem
class OrderItemInline(admin.TabularInline):
    # Specify the model this inline admin class is for
    model = models.OrderItem
    # Set the number of empty formsets to display
    extra = 1

# Define a model admin class for Order


class OrderAdmin(admin.ModelAdmin):
    # Specify inline admin classes to display on the Order detail page
    inlines = [
        OrderItemInline,
    ]


# Register Order with OrderAdmin
admin.site.register(models.Order, OrderAdmin)

# Register OrderItem directly
admin.site.register(models.OrderItem)
