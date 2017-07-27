from django.conf.urls import url

from agenda import views
from agenda.views import RemarcarCompromissoView, MarcarCompromissoView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compromisso/(?P<compromisso_id>\d+)$', views.detalhesDoCompromisso, name='compromisso'),
    url(r'^compromisso/(?P<compromisso_id>\d+)/cancelar$', views.cancelarCompromisso, name='cancelarCompromisso'),
    url(r'^compromisso/(?P<compromisso_id>\d+)/concluir$', views.concluirCompromisso, name='concluirCompromisso'),
    url(r'^compromisso/(?P<compromisso_id>\d+)/iniciar$', views.iniciarCompromisso, name='iniciarCompromisso'),
    url(r'^compromisso/(?P<compromisso_id>\d+)/remarcar$', RemarcarCompromissoView.as_view(), name='remarcarCompromisso'),
    url(r'^compromisso/(?P<escritorio_id>\d+)/marcar$', MarcarCompromissoView.as_view(), name='marcarCompromisso'),
    url(r'^perfil/(?P<perfil_id>\d+)$', views.detalhesPerfil, name='perfil'),
    url(r'^perfil/(?P<perfil_id>\d+)/ficarAusente$', views.ficarAusente, name='ficarAusente'),
    url(r'^perfil/(?P<perfil_id>\d+)/ficarPresente$', views.ficarPresente, name='ficarPresente'),
]