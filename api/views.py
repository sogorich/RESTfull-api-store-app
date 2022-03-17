from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Cart, Product, ProductInCart
from .serializers import ProductInCartSerializer, ProductSerializer
from .permissions import IsOwnerProductInCart

from .mixins import PermissionIndividualActionsViewSetMixin
from .services import get_all_or_filter, get_object_or_none


class ProductViewSet(PermissionIndividualActionsViewSetMixin, viewsets.ModelViewSet):
    """ Представление данных о товарах. """

    queryset = get_all_or_filter(Product)
    serializer_class = ProductSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes_for_actions = {
        **dict.fromkeys(('create', 'update', 'partial_update', 'destroy'), (IsAdminUser,))
    }


class ProductInCartViewSet(PermissionIndividualActionsViewSetMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    """ Представление данных о товарах в корзинах покупателей. """

    queryset = get_all_or_filter(ProductInCart)
    serializer_class = ProductInCartSerializer

    permission_classes = (IsAuthenticated, IsOwnerProductInCart)

    def perform_create(self, serializer) -> dict | None:

        query = get_all_or_filter(ProductInCart, cart__customer_id=self.request.user.pk,
                                  product_id=serializer.validated_data['product'].pk)

        if query.exists():
            return {'error_message': 'Такой товар уже добавлен в Вашу корзину, если нужно больше одного товара перейдите в корзину и увеличте его количество.'}

        else:
            serializer.validated_data['cart'] = get_object_or_none(
                Cart, customer_id=self.request.user.pk)

            serializer.save()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        perform_create_result = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        if perform_create_result is None:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(perform_create_result, status=status.HTTP_400_BAD_REQUEST)
