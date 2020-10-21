# -*- coding: utf-8 -*-
import datetime

from rest_framework.exceptions import AuthenticationFailed

from . import logger
from recruit.utils import parser
from rest_framework import permissions
from django.contrib.auth import get_user_model
from recruit.models import RespondentToken, Respondents
from wechatRecruit.settings import RESPONDENT_TOKEN_EXPIRED
UserModel = get_user_model()


class CheckTokenPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        token = request.data.get('token')
        if request.data.get('token'):
            try:
                respondents_id = int(token.split('&')[-1])
                token_obj = RespondentToken.objects.get(key=token, respondents_id=respondents_id)
            except Exception as e:
                logger.error(e)
                raise AuthenticationFailed(str(e))
            token_created_time = int(parser.string2time_stamp(str(token_obj.create_time)))
            now = int(parser.string2time_stamp(str(datetime.datetime.now())))
            # 满足条件的话，就表示token已失效，提示用户重新登录刷新token.
            if now - token_created_time > RESPONDENT_TOKEN_EXPIRED:
                token_obj.status = True
                token_obj.save()
                raise AuthenticationFailed('Token has expired')
            return True
        if view.__class__.__name__ == 'RespondentsView' and view.action == 'post':
            return True
        if request.user.is_authenticated:
            return True
        return False

