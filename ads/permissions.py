from django.http import Http404
from rest_framework import permissions

from ads.models import Ad, Selection
from users.models import User


class SelectionUpdatePermission(permissions.BasePermission):
    message = 'Для управления подборками не достаточно прав.'

    def has_permission(self, request, view):
        try:
            entity = Selection.objects.get(pk=view.kwargs["pk"])
        except Selection.DoesNotExist:
            raise Http404

        if entity.owner_id == request.user.id:
            return True
        return False


class AdUpdatePermission(permissions.BasePermission):
    message = "Для управления объявлениями не достаточно прав."

    def has_permission(self, request, view):
        if request.user.role in [User.MEMBER, User.ADMIN]:
            return True
        try:
            entity = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            raise Http404

        if entity.author_id == request.user.id:
            return True
        return False