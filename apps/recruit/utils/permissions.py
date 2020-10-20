# -*- coding: utf-8 -*-
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework import status

from recruit.models import RespondentToken

UserModel = get_user_model()


class CheckTokenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if request.data.get('token'):
            return True
        if view.__class__.__name__ == 'RespondentsView' and view.action == 'post':
            return True
        if request.user.is_authenticated:
            return True
        return False

