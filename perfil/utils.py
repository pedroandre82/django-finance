from extrato.models import Valores
from datetime import datetime
from contas.models import ContaPaga, ContaPagar


def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)

    return total


def calcula_equilibrio_financeiro() -> tuple[str, str]:
    gastos = (
        Valores.objects
        .filter(data__month=datetime.now().month)
        .filter(tipo='S')
    )
    gastos_essenciais = gastos.filter(categoria__essencial=True)  # Foreign key
    gastos_nao_essenciais = gastos.filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais

    if total == 0:
        return 0, 0
    
    percentual_gastos_essenciais = round(total_gastos_essenciais * 100 / total, 1)

    # Garantir que a soma das porcentagens seja 100
    percentual_gastos_nao_essenciais = 100 - percentual_gastos_essenciais

    return f"{percentual_gastos_essenciais:.01f}", f"{percentual_gastos_nao_essenciais:.01f}"


def contas_pagas():
    mes = datetime.now().month
    return (
        ContaPaga.objects
        .filter(data_pagamento__month=mes)
        .values('conta')
    )

def contas_vencidas():
    dia: int = datetime.now().day
    return (
        ContaPagar.objects.all()
        .filter(dia_pagamento__lt=dia)
        .exclude(id__in=contas_pagas())
    )

def contas_proximas_vencimento(periodo: int = 5):
    dia: int = datetime.now().day
    return (
        ContaPagar.objects.all()
        .filter(dia_pagamento__gte=dia)
        .filter(dia_pagamento__lte=dia+periodo)
        .exclude(id__in=contas_pagas())
    )

def contas_restantes():
    return (
        ContaPagar.objects.all()
        .exclude(id__in=contas_vencidas())
        .exclude(id__in=contas_pagas())
        .exclude(id__in=contas_proximas_vencimento())
    )
