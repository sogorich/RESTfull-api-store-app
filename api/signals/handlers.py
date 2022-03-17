from rest_framework.authtoken.models import Token

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from api.models import Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_dependencies_for_new_user(sender, **kwargs) -> None:
    """
        Сигнал реализует необходимые зависимости в момент создания нового
        пользователя. Создаётся объект корзины и генерируется токен.
    """

    if kwargs['created']:

        Cart.objects.create(customer=kwargs['instance'])
        Token.objects.create(user=kwargs['instance'])
