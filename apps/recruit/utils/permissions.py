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
        return True

