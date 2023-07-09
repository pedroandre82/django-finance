from django.db import models
from django.db.models import Sum
from datetime import datetime

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = (
            Valores.objects
            .filter(categoria__id = self.id)
            .filter(data__month=datetime.now().month)
            .filter(tipo='S')
            .aggregate(Sum('valor'))
        )
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    @property
    def total_gasto_str(self):
        return f"{self.total_gasto():,.02f}"
    
    @property
    def valor_planejamento_str(self):
        return f"{self.valor_planejamento:,.02f}"

    def calcula_percentual_gasto_por_categoria(self):
        if self.valor_planejamento == 0:
            return 0

        return int(100 * self.total_gasto() / self.valor_planejamento)
    
    def total_recebido(self):
        from extrato.models import Valores
        valores = (
            Valores.objects
            .filter(categoria__id = self.id)
            .filter(data__month=datetime.now().month)
            .filter(tipo='E')
            .aggregate(Sum('valor'))
        )
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    def total_recebido_str(self):
        return f"{self.total_recebido:,.02f}"


class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('BB', 'Banco do Brasil'),
        ('BR', 'Bradesco'),
    )

    tipo_choices = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido
