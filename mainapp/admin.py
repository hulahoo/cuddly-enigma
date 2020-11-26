"""Админка"""
from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image


class ImageForm(ModelForm):
    """Устанавливаем стандартное разрешение для картинок"""
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)

    def __init__(self, *args, **kwargs):
        """Переорпределяем роидтельский класс"""
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; font-size:14px;">Загружайте изображения с минимальным расширением: {}x{}</span>'.format(
                *self.MIN_RESOLUTION
            ))

        def clean_image(self):
            image = self.cleaned_data['image']
            img = Image.open(image)
            min_height, min_width = self.MIN_RESOLUTION
            max_height, max_width = self.MAX_RESOLUTION
            if img.height < min_height or img.width < min_width:
                raise ValidationError('Загруженное изрображение меньше минимального разрешения')
            if img.height < max_height or img.width < max_width:
                raise ValidationError('Загруженное изрображение больше максимального разрешения')
            return image
            print(img.width, img.height)
            return image

class ImageInline(admin.TabularInline):
    """Это админка для картинки"""
    model = ProductImage
    extra = 1
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
admin.site.register(Comment)
admin.site.register(CartProduct)
admin.site.register(Cart)
