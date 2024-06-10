"""
URL configuration for GdsSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserCreateView
from GdsSystem.views import PerfilAPI, ProjetoAPI, ProjetoUsuarioAPI


urlpatterns = [
    path('admin', admin.site.urls),
    path('token', obtain_auth_token, name='token'),
    path('create_user', UserCreateView.as_view(), name='create_user'),
    path('perfil', PerfilAPI.as_view(), name='perfil'),
    path('perfil/<pk>', PerfilAPI.as_view(), name='perfil'),
    path('projeto', ProjetoAPI.as_view(), name='projeto'),
    path('projeto/<pk>', ProjetoAPI.as_view(), name='projeto'),
    path('projeto_usuario', ProjetoUsuarioAPI.as_view(), name='projeto_usuario'),
    path('projeto_usuario/<pk>', ProjetoUsuarioAPI.as_view(), name='projeto_usuario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
