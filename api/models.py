from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class DateTimeFieldsModel(models.Model):
    """ 
        Абстрактная модель, определяющая 2 поля типа datetime. 
        created - дата и время создания записи;
        updated - дата и время обновления записи.
    """

    created = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    class Meta:
        abstract = True


class Product(DateTimeFieldsModel):
    """ Модель товара. """

    title = models.CharField('Название товара', max_length=256, db_index=True)
    spoiler = models.CharField(
        'Краткое описание товара', max_length=256, blank=True)
    desc = models.TextField('Описание товара', blank=True)
    product_photo = models.ForeignKey(
        'Photo', on_delete=models.CASCADE, verbose_name='Фото товара', related_name='prod_photo', null=True)
    available = models.BooleanField('Наличие на складе', default=False)
    qty = models.PositiveIntegerField(
        'Количество товаров на складе', default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Photo(DateTimeFieldsModel):
    """ Модель фотографии товара. """

    photo = models.ImageField('Фото товара', upload_to='photos/%d/%m/%Y')

    updated = None

    def __str__(self) -> str:
        return f'Фотография ID: {self.pk}'

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'


class Cart(models.Model):
    """ Модель корзины. """

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 verbose_name='Покупатель', related_name='cart_customer')
    products = models.ManyToManyField(
        Product, through='ProductInCart', through_fields=('cart', 'product'))

    def __str__(self) -> str:
        return f'Корзина покупателя {self.customer.username}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Сформированные корзины покупателей'


class ProductInCart(models.Model):
    """ 
        Промужеточная модель между корзиной и товарами. Реализует дополнительное
        поле - количество конкретного товара в корзине. 
    """

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='user_cart')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт')
    prod_count = models.PositiveIntegerField(
        'Количество', default=1, validators=[MaxValueValidator(10, 'В корзину допустимо добавить только 10 единиц одного товара.'), MinValueValidator(1, 'Значение не должно быть меньше единицы.')])

    def __str__(self) -> str:
        return f'В корзине покупателя {self.cart.customer} находится товар {self.product} (x{self.prod_count})'

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
