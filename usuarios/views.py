from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from agenda.models import Profissional
from agenda.views import perfilLogado
from usuarios.forms import RegistrarForm

@login_required
def novoProfissional(request):
    profissional = perfilLogado(request)
    if profissional.escritorio != None:
        return redirect('index')
    return render(request, 'novo_profissional.html')


class RegistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            usuario = User.objects.create_user(username=dados['nome'].replace(" ", "_").lower(),
                                      email=dados['email'],
                                      password=dados['senha'])

            Profissional.objects.create(nome=dados['nome'],
                                        telefone=dados['telefone'],
                                        profissao=dados['profissao'],
                                                       usuario=usuario)

            return redirect('login')
        return render(request, self.template_name, {'form': form})