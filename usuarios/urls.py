from django.conf.urls import url

from usuarios import views
from usuarios.views import RegistrarUsuarioView

urlpatterns = [
    url(r'^registrar/$', RegistrarUsuarioView.as_view(), name="registrar"),
    url(r'^novo/$', views.novoProfissional, name="novoProfissional")
]