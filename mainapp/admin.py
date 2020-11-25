"""Админка"""
from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    """Это админка для картинки"""
    model = ProductImage
    extra = 0
    fields = ('image', )


class ProductAdmin(admin.ModelAdmin):
    """Это админка продкута. Здесь мы костомизируеем модельку"""
    inlines = [
        ImageInline,
    ]
    list_display = ('id', 'title')  # по нажатию мы переходим на сам продукт
    list_display_links = ('id', 'title')  # те поля с помощью которых можно попасть на описания продукта


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart)
