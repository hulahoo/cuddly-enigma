"""В моделях мы будем создавать категории продукты корзины"""
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now

User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})
    

class Category(models.Model):
    """Создание модели категории"""
    name = models.CharField(max_length=250, verbose_name='Category name')  # category name это человеку улобочитаемое название поля
    slug = models.SlugField(unique=True)  # создаем уникальный ключ под названием slug который модель которого выглядит так models.SlugField и передаем ему уникальное значение

    def __str__(self):
        """выводим удобочитаемый текст для пользователя"""
        return self.name


class Product(models.Model):
    """Здесь мы создаем модель продуктов"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')  # здесь мы привязываем наш класс продуктов к классу категорий и при удалении категории по логике удаляються все продукты данной категории
    title = models.CharField(max_length=255, verbose_name='Title')  # здесь мы создаем заголовок продукта
    slug = models.SlugField(unique=True, verbose_name='Unique name')  # здесь мы создаем уникальное название продукта
    image = models.ImageField(verbose_name='Image of Product')  # здесь мы создаем место для добавления картинок
    description = models.TextField(verbose_name='Description', blank=True)  # здесь мы создаем описание для продукта из TextField и описание также может быть пустым
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Price')  # здесь мы создаем цену и указываем DecimalField
    release_date = models.DateTimeField(default=now, verbose_name='release date')
    def __str__(self):
        """выводим удобочитаемый текст для пользователя"""
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=5)



class ProductImage(models.Model):
    """Здесь мы делаем модель для картинки"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)


class CartProduct(models.Model):
    """Здесь мы создаем класс продуктов корзины"""
    user = models.ForeignKey('Customer', verbose_name='Username', on_delete=models.CASCADE)  # здесь мы создаем пользователя который заказал продукт
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')  # здесь мы создаем саму корзину
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)  # здесь мы создаем сам продукт который пользователь закинул в корзину и привязка идет к Product
    amount = models.PositiveIntegerField(default=1)  # здесь мы создаем количество данного продукта, и его количество по стандарту равняется 1
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Price')  # здесь мы указываем полную цену всех наших продуктов которые находятся в корзине

    def __str__(self):
        """выводим удобочитаемый текст для пользователя"""
        return f'Cart Product: {self.product.title}'  # выводим имя нашего продукта


class Cart(models.Model):
    """Здесь мы создаем саму корзину"""
    owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)  # здесь мы указываем владельца корзины
    products = models.ManyToManyField(CartProduct, related_name='related_cart')  # здесь мы указываем продукты со связью m2m потому что в одной корзине может быть несколько продуктов и несколько одинаковых продуктов могут быть в одной корзине
    total_products = models.PositiveIntegerField(default=0)  # здесь мы создаем общее количество уникальных продуктов по станадарту у нас их там 0
    final_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total Price')

    def __str__(self):
        """выводим удобочитаемый текст для пользователя"""
        return str(self.id)


class Customer(models.Model):
    """Создаем ппокупателя"""
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)  # здесь мы создаем самого пользователя
    first_name = models.CharField(max_length=255, verbose_name="User's name")  # здесь мы создаем имя пользователя
    phone = models.CharField(max_length=20, verbose_name="User's phone")  # здесь мы создаем номер телефона пользователя
    address = models.CharField(max_length=255, verbose_name='Address')  # здесь мы создаем адрес пользователя

    def __str__(self):
        return f"Customer: {self.user.last_name} {self.user.first_name}"

# TODO: Создание модели Заказа
# TODO: Создание модели Specification
