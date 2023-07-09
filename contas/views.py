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
    return render(
        request=request, 
        template_name='ver_contas.html', 
        context={'contas_vencidas': contas_vencidas(), 
                'contas_proximas_vencimento': contas_proximas_vencimento(), 
                'restantes': contas_restantes(),
                'contas_pagas': contas_pagas,
                }
    )


def pagar_conta(request, id):
    conta = ContaPaga(
        conta_id = id,
        data_pagamento = datetime.now()
    )
    conta.save()

    messages.add_message(
        request=request,
        level=constants.SUCCESS,
        message=f"Conta paga com sucesso."
    )
    return redirect('/contas/ver_contas')

    