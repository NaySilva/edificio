from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from agenda.models import Profissional
from agenda.views import perfilLogado
from usuarios.forms import RegistrarForm

def novoProfissional(request):
    profissional = perfilLogado()
    if profissional.escritorio:
        return redirect('index')
    return render(request, 'novo_profissional.html')

class RegistrarUsuarioView(View):
    template_name = 'registrar.html'
    perfil = perfilLogado()
    def get(self, request):
        if self.perfil:
            return redirect('index')
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            usuario = User.objects.create(username=dados['nome'],
                                      email=dados['email'],
                                      password=dados['senha'])

            profissional = Profissional.objects.create(nome=dados['nome'],
                                                       telefone=dados['telefone'],
                                                       profissao=dados['profissao'],
                                                       usuario=usuario)
            print(profissional)
            print(usuario)
            return redirect('novoProfissional')
        return render(request, self.template_name, {'form': form})