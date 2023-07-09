from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPaga, ContaPagar
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from perfil.utils import contas_pagas, contas_proximas_vencimento, contas_restantes, contas_vencidas

# Create your views here.

def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(
            request=request,
            template_name='definir_contas.html',
            context={"categorias": categorias}
        )
    else:
        titulo = request.POST.get("titulo")
        categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        dia_pagamento = request.POST.get("dia_pagamento")

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento,
        )
        conta.save()

        messages.add_message(
            request=request,
            level=constants.SUCCESS,
            message="Conta adicionada com sucesso."
        )

        return redirect("definir_contas")
    

def ver_contas(request):
    # MES_ATUAL = datetime.now().month
    # DIA_ATUAL = datetime.now().day
    
    # contas = ContaPagar.objects.all()

    # contas_pagas = (
    #     ContaPaga.objects
    #     .filter(data_pagamento__month=MES_ATUAL)
    #     .values('conta')
    # )
    # contas_vencidas = (
    #     contas
    #     .filter(dia_pagamento__lt=DIA_ATUAL)
    #     .exclude(id__in=contas_pagas)
    # )
    # contas_proximas_vencimento = (
    #     contas
    #     .filter(dia_pagamento__lte=DIA_ATUAL+5)  # IDEA: personalizar esse período
    #     .filter(dia_pagamento__gte=DIA_ATUAL)
    #     .exclude(id__in=contas_pagas)
    # )
    # restantes = (
    #     contas
    #     .exclude(id__in=contas_vencidas)
    #     .exclude(id__in=contas_pagas)
    #     .exclude(id__in=contas_proximas_vencimento)
    # )

    return render(
        request=request, 
        template_name='ver_contas.html', 
        context={'contas_vencidas': contas_vencidas(), 
                 'contas_proximas_vencimento': contas_proximas_vencimento(), 
                 'restantes': contas_restantes(),
                 'contas_pagas': contas_pagas,
                }
    )
