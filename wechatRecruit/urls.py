"""wechatRecruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework.authtoken import views
from constance.admin import admin
from wechatRecruit import settings
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('xadmin/database/constance/', admin.site.urls),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/user/login/', obtain_jwt_token),
    path(r'recruit/', include('recruit.urls')),
]
