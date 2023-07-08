from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from perfil.models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .models import Valores
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO
# from .utils import calcula_total

# Create your views here.

def novo_valor(request):
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all() 
        return render(
            request=request, 
            template_name='novo_valor.html',
            context={'contas': contas,
                     'categorias': categorias,
                     }
            )
    
    elif request.method == "POST":
        valor = request.POST.get("valor")
        conta = request.POST.get("conta")
        tipo = request.POST.get("tipo")
        
        valores = Valores(
            valor=valor,
            categoria_id=request.POST.get("categoria"),
            descricao=request.POST.get("descricao"),
            data=request.POST.get("data"),
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)
        if tipo == 'E':
            conta.valor += int(valor)
            msg = "Entrada"
        else:
            conta.valor -= int(valor)
            msg = "Saída"
        conta.save()

        messages.add_message(
            request=request,
            level=constants.SUCCESS, 
            message=f'{msg} cadastrada com sucesso'
        )

        return redirect('/extrato/novo_valor')


def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    conta_get = request.GET.get('conta')   
    categoria_get = request.GET.get('categoria')
    valores = Valores.objects.filter(data__month=datetime.now().month)
 
    if conta_get is not None:
        valores = valores.filter(conta__id=conta_get)

    if categoria_get is not None:
        valores = valores.filter(categoria__id=categoria_get)

# TODO: clear fields
# TODO: add period filter

    return render(
        request=request,
        template_name='view_extrato.html',
        context={'valores': valores, 
                 'contas': contas, 
                 'categorias': categorias,
                 }
    )


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(
        template_name=path_template,
        context={"valores": valores},
    )
    path_output = BytesIO()
    HTML(string=template_render).write_pdf(target=path_output)
    path_output.seek(0)
    return FileResponse(path_output, filename="extrato.pdf")
