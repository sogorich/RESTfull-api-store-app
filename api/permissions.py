from rest_framework import permissions


class IsOwnerProductInCart(permissions.BasePermission):
    """ Взаимодействовать с продуктами в корзине могут только те кто их добавил. """

    def has_object_permission(self, request, view, obj) -> bool:

        return obj.cart.customer_id == request.user.pk
