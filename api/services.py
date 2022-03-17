from django.db.models.base import Model
from django.db.models import QuerySet

from django.core.exceptions import ObjectDoesNotExist

from typing import Any


def get_all_or_filter(model: Model, **kwargs: Any) -> QuerySet:
    """ 
        Возвращает QuerySet с результатом выборки по указанным фильтрам, если
        фильтры отсутствуют - возвращаются все записи. 
    """

    return model.objects.filter(**kwargs) if kwargs else model.objects.all()


def get_object_or_none(model: Model, **kwargs: Any) -> object | None:
    """ 
        Возращает объект записи из базы даных, при отсутствии объекта возвращается None. 
    """
    try:
        object_ = model.objects.get(**kwargs)

    except ObjectDoesNotExist:
        object_ = None

    return object_
