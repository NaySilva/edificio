from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from requests import request

from agenda.forms import RemarcarForm, MarcarForm, EditarPerfilForm, RegistrarEscritorioForm, AdicionarProfissionalForm, \
    AdicionarSalaForm
from agenda.models import Escritorio, Profissional, Sala, ItemAgenda, Cliente

@login_required
def index(request):
    perfil = perfilLogado(request)
    print(perfil.escritorio)
    if perfil.escritorio == None:
        return redirect('novoProfissional')
    escritorio = perfil.escritorio
    profissionais = Profissional.objects.filter(escritorio=escritorio)
    salas = Sala.objects.filter(escritorio=escritorio)
    compromissos = ItemAgenda.objects.filter(escritorio=escritorio, data=date.today()).order_by('horario')
    return render(request,'index.html', {'escritorio':escritorio, 'profissionais':profissionais, 'salas':salas,
                                         'compromissos':compromissos, 'perfilLogado':perfil})

@login_required
def perfilLogado(request):
    return request.user.profissional

@login_required
def detalhesDoCompromisso(request, compromisso_id):
    compromisso = ItemAgenda.objects.get(id=compromisso_id)
    return render(request, 'compromisso.html', {'compromisso':compromisso, 'perfilLogado':perfilLogado(request)})

@login_required
def cancelarCompromisso(request, compromisso_id):
    compromisso = ItemAgenda.objects.get(id=compromisso_id)
    compromisso.mudar_situacao('C')
    compromisso.profissional.mudar_status('D')
    return redirect('compromisso', compromisso_id=compromisso_id)

@login_required
def iniciarCompromisso(request, compromisso_id):
    compromisso = ItemAgenda.objects.get(id=compromisso_id)
    compromisso.mudar_situacao('E')
    compromisso.profissional.mudar_status('O')
    return redirect('compromisso', compromisso_id=compromisso_id)

@login_required
def concluirCompromisso(request, compromisso_id):
    compromisso = ItemAgenda.objects.get(id=compromisso_id)
    compromisso.mudar_situacao('R')
    compromisso.profissional.mudar_status('D')
    return redirect('compromisso', compromisso_id=compromisso_id)

class RemarcarCompromissoView(View):
    template_name = 'compromisso.html'

    @login_required
    def get(self, request):
        return render(request, self.template_name)

    @login_required
    def post(self, request, compromisso_id):
        print(compromisso_id)
        form = RemarcarForm(request.POST)
        compromisso = ItemAgenda.objects.get(id=compromisso_id)
        if form.is_valid():
            dados = form.cleaned_data
            print(dados)
            compromisso.remarcar(data=dados['data'],hora=dados['horario'])
            return redirect('index')
        return render(request, self.template_name, {'form': form, 'compromisso':compromisso, 'perfilLogado':perfilLogado(request)})

class AdicionarProfissionalView(View):
    template_name = 'gerenciar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = AdicionarProfissionalForm(request.POST)
        escritorio = perfilLogado(request).escritorio
        if form.is_valid():
            dados = form.cleaned_data
            print(dados)
            profissional = Profissional.objects.filter(usuario__username=dados['username']).first()
            profissional.escritorio = escritorio
            profissional.save(force_update=True)
        return redirect('gerenciar')


@login_required
def removerProfissional(request, profissional_id):
    profissional = Profissional.objects.get(id=profissional_id)
    profissional.escritorio = None
    profissional.save(force_update=True)
    return redirect('gerenciar')

@login_required
def excluirPerfil(request):
    profissional = perfilLogado(request)
    escritorio = profissional.escritorio
    profissional.usuario.delete()
    profissional.delete()
    profissional = Profissional.objects.filter(escritorio=escritorio).first()
    if profissional:
        profissional.gerente = True
        profissional.save(force_update=True)
    else:
        escritorio.delete()
    return redirect('login')

@login_required
def removerSala(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    sala.escritorio = None
    sala.save(force_update=True)
    return redirect('gerenciar')

class AdicionarSalaView(View):
    template_name = 'gerenciar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = AdicionarSalaForm(request.POST)
        escritorio = perfilLogado(request).escritorio
        if form.is_valid():
            dados = form.cleaned_data
            print(dados)
            Sala.objects.create(numero=dados['numero'],
                            andar=dados['andar'],
                            escritorio=escritorio)
        return redirect('gerenciar')

class EditarPerfilView(View):
    template_name = 'perfil.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, perfil_id):
        form = EditarPerfilForm(request.POST)
        perfil = Profissional.objects.get(id=perfil_id)
        if form.is_valid():
            dados = form.cleaned_data
            perfil.editar_perfil(nome = dados['nome'],
                                 profissao = dados['profissao'],
                                 telefone = dados['telefone'])
            return redirect('perfil', perfil_id=perfil_id)
        return render(request, self.template_name, {'form': form, 'perfil':perfil, 'perfilLogado':perfilLogado(request)})

class MarcarCompromissoView(View):

    template_name = 'compromisso.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'perfil.html', {'perfilLogado': perfilLogado(request)})

    def post(self, request, *args, **kwargs):
        form = MarcarForm(request.POST)
        escritorio_id = kwargs['escritorio_id']
        escritorio = Escritorio.objects.get(id=escritorio_id)
        if form.is_valid():
            dados = form.cleaned_data
            print(dados)
            cliente = Cliente.objects.filter(cpf=dados['cpf']).first()
            if cliente:
                cliente.nome = dados['nome']
                cliente.telefone = dados['telefone']
                cliente.save(force_update=True)
            else:
                cliente = Cliente.objects.create(cpf=dados['cpf'],nome=dados['nome'],telefone=dados['telefone'])
            profissional = Profissional.objects.get(nome=dados['profissional'],escritorio=escritorio)
            compromisso = ItemAgenda.objects.create(cliente=cliente,
                                      escritorio=escritorio,
                                      profissional=profissional,
                                      data=dados['data'],
                                      horario=dados['horario'])
            return redirect('compromisso', compromisso_id=compromisso.id)
        return redirect('index')


@login_required
def detalhesPerfil(request, perfil_id):
    perfil = Profissional.objects.get(id=perfil_id)
    escritorio = perfil.escritorio
    profissionais = Profissional.objects.filter(escritorio=escritorio)
    clientes = Cliente.objects.all()
    compromissos = ItemAgenda.objects.filter(profissional=perfil, data=date.today()).order_by('horario')
    return render(request, 'perfil.html', {'perfil':perfil, 'perfilLogado':perfilLogado(request),
                                           'escritorio':escritorio, 'profissionais':profissionais,
                                           'clientes':clientes, 'compromissos':compromissos})


@login_required
def ficarAusente(request, perfil_id):
    perfil = Profissional.objects.get(id=perfil_id)
    perfil.mudar_status('A')
    return redirect('perfil', perfil_id=perfil_id)

@login_required
def ficarPresente(request, perfil_id):
    perfil = Profissional.objects.get(id=perfil_id)
    perfil.mudar_status('D')
    return redirect('perfil', perfil_id=perfil_id)

@login_required
def detalhesAgenda(request, filter='data'):
    escritorio = perfilLogado(request).escritorio
    proximosCompromissos = ItemAgenda.objects.filter(escritorio=escritorio, situacao='A').order_by('data', 'horario')
    todosCompromissos = ItemAgenda.objects.filter(escritorio=escritorio).order_by(filter, 'data', 'horario')
    return render(request, 'agenda.html', {'proxCompromissos':proximosCompromissos,
                                           'todosCompromissos':todosCompromissos,
                                           'perfilLogado': perfilLogado(request)})

@login_required
def gerenciarEscritorio(request):
    escritorio = perfilLogado(request).escritorio
    profissionais = Profissional.objects.filter(escritorio=escritorio)
    salas = Sala.objects.filter(escritorio=escritorio)
    return render(request, 'gerenciar.html', {'profissionais':profissionais,
                                              'salas': salas,
                                              'perfilLogado': perfilLogado(request)})



class RegistrarEscritorioView(View):
    template_name = 'registrar_escritorio.html'

    def get(self, request):
        perfil = perfilLogado(request)
        if perfil.escritorio != None:
            redirect('index')
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarEscritorioForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            escritorio = Escritorio.objects.create(nome_escritorio=dados['nome'],
                                                   servico=dados['servico'])
            Sala.objects.create(numero=dados['numero'],
                                      andar=dados['andar'],
                                      escritorio = escritorio)
            perfil = perfilLogado(request)
            perfil.escritorio = escritorio
            perfil.gerente = True
            perfil.save(force_update=True)
            return redirect('index')
        return render(request, self.template_name, {'form': form})