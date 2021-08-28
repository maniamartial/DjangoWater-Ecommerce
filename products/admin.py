from products.views import waterSamples
from django.contrib import admin
from django.contrib.admin.decorators import register

# Register your models here.
from .models import Category, Order, OrderItem, Product, ShippingAddress


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_published', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('price', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'price')
    ordering = ('price',)
    #exclude = ('description',)


# Registering the water Products
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

# Registering the water categories
'''admin.site.register(water_categories)
admin.site.register(Water_Types)

# Registering the services
admin.site.register(water_services_category)
admin.site.register(Water_Services)'''

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
