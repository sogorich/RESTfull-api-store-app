from rest_framework import serializers

from .models import Product, ProductInCart


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор модели товара. """

    class Meta:
        model = Product
        fields = ('title', 'spoiler', 'desc',
                  'available', 'qty', 'product_photo')


class ProductInCartSerializer(serializers.ModelSerializer):
    """ Серализатор модели товаров в корзине. """

    customer = serializers.SerializerMethodField(
        method_name='get_customer_read_only')

    def get_customer_read_only(self, obj) -> str | None:
        try:
            customer = obj.cart.customer.username

        except (AttributeError, Exception):
            customer = None

        return customer

    class Meta:
        model = ProductInCart
        fields = ('customer', 'product', 'prod_count')
