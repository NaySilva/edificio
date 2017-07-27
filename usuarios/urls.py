from django.conf.urls import url

from usuarios import views
from usuarios.views import RegistrarUsuarioView

urlpatterns = [
    url(r'^registrar/$', RegistrarUsuarioView.as_view(), name="registrar"),
    url(r'^novo/$', views.novoProfissional, name="novoProfissional"),
    url(r'^login/$',views.LoginView.as_view(template_name='login.html'), name = 'login'),
    url(r'^logout/$', views.LogoutView.as_view(template_name='login.html'), name="logout"),
]