from extrato.models import Valores
from datetime import datetime


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
