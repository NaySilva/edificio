from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=10)
    cpf = models.CharField(max_length=11)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'Cliente %s' % (self.nome)


class Escritorio(models.Model):
    nome_escritorio = models.CharField(max_length=120)
    servico = models.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.nome_escritorio

    def agendar(self, profissional, cliente, data, hora):
        agenda = ItemAgenda()
        agenda.profissional = profissional
        agenda.cliente = cliente
        agenda.data = data
        agenda.horario = hora
        agenda.save(force_insert=True)


class Sala(models.Model):
    numero = models.CharField(max_length=3)
    andar = models.CharField(max_length=2)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='salas', null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.numero

class Profissional(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=10)
    profissao = models.CharField(max_length=120)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name="profissionais", null=True)
    gerente = models.BooleanField(default=False)
    STATUS = (
        ('A', 'Ausente'),
        ('D', 'Disponível'),
        ('O', 'Ocupado'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default='A')
    usuario = models.OneToOneField(User, related_name="profissional", on_delete=models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'Profissional %s' % (self.nome)

    def mudar_status(self, opcao):
        self.status = opcao
        self.save(force_update=True)

    def editar_perfil(self, nome, profissao, telefone):
        self.nome = nome
        self.profissao = profissao
        self.telefone = telefone
        self.save(force_update=True)


class ItemAgenda(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='agenda_profissionais')
    horario = models.TimeField()
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agenda_cliente')
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='agenda_escritorio')
    SITUACAO = (
        ('A','Agendado'),
        ('R','Realizado'),
        ('C','Cancelado'),
        ('E','Em Andamento'),
    )
    situacao = models.CharField(max_length=1, choices=SITUACAO, default='A')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.cliente, self.profissional)

    def mudar_situacao(self, opcao):
        self.situacao = opcao
        self.save(force_update=True)

    def remarcar(self, data, hora):
        ItemAgenda.objects.create(
            profissional = self.profissional,
            cliente = self.cliente,
            horario = hora,
            data = data,
            escritorio = self.escritorio)
        self.mudar_situacao('C')