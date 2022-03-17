from .views import ProductInCartViewSet, ProductViewSet
from django.urls import path, include

from rest_framework import routers


router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('prod_in_cart', ProductInCartViewSet, basename='prod_in_cart')


urlpatterns = [
    path('', include(router.urls)),
]
