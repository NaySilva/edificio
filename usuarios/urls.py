from django.conf.urls import url

from usuarios import views as uv
from django.contrib.auth import views

from usuarios.views import RegistrarUsuarioView

urlpatterns = [
    url(r'^registrar/$', RegistrarUsuarioView.as_view(), name="registrar"),
    url(r'^novo/$', uv.novoProfissional, name="novoProfissional"),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'login.html'}, name='logout'),
]