from rest_framework import viewsets


class PermissionIndividualActionsViewSetMixin(viewsets.GenericViewSet):
    """ 
        Миксин, позволяющий устанавливать ограничения на 
        отдельные действия внутри ViewSet. 
    """

    permission_classes_for_actions = {}

    def get_permissions(self):

        try:
            return [permission() for permission in self.permission_classes_for_actions[self.action]]

        except Exception:
            return super().get_permissions()
