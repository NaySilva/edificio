from django.db import models

# Create your models here.



class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=10)
    cpf = models.IntegerField(11)

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
    profissão = models.CharField(max_length=120)
    disponivel = models.BooleanField()
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name="profissionais")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disponivel = False

    def __str__(self):
        return 'Profissional %s' % (self.nome)

    def mudar_status(self):
        self.disponivel = not self.disponivel
        self.save(force_update=True)


class ItemAgenda(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='agenda_profissional')
    horario = models.TimeField()
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agenda_cliente')
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='agenda_escritorio')
    SITUACAO = (
        ('A','Agendada'),
        ('R','Realizada'),
        ('C','Cancelada'),
    )
    situacao = models.CharField(max_length=1, choices=SITUACAO)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.situacao = 'A'

    def __str__(self):
        return '%s - %s (%s)' % (self.cliente, self.profissional, self.escritorio)

    def mudar_situacao(self, opcao):
        self.situacao = opcao
        self.save(force_update=True)

    def remarcar(self, data, hora):
        agenda = ItemAgenda()
        agenda.profissional = self.profissional
        agenda.cliente = self.cliente
        agenda.horario = hora
        agenda.data = data
        agenda.save(force_insert=True)
        self.mudar_situacao('C')