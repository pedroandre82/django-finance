from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total

# Create your views here.
def home(request):
    contas = Conta.objects.all()
    total_contas = calcula_total(contas, "valor")
    categorias = Categoria.objects.all()

    return render(request=request, 
                  template_name="home.html",
                  context={'contas': contas,
                           'total_contas': total_contas,
                           })


def gerenciar(request):
    contas = Conta.objects.all()
    total_contas = calcula_total(contas, "valor")
   
    categorias = Categoria.objects.all()

    return render(
        request=request, 
        template_name="gerenciar.html",
        context={'contas': contas,
                 'total_contas': total_contas,
                 'categorias': categorias}
    )


def cadastrar_banco(request):
    apelido=request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    # validar dados
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message="Preencha todos os campos"
        )
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )
    conta.save()
    messages.add_message(
        request=request,
        level=constants.SUCCESS,
        message="Conta cadastrada com sucesso"
    )

    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(
        request=request,
        level=constants.SUCCESS,
        message="Conta deletada com sucesso"
    )
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message="Adicione um nome para a categoria"
        )
        return redirect('/perfil/gerenciar/')
    
    if not isinstance(essencial, bool):
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message="Erro com o campo \"Essencial\""
        )
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    messages.add_message(
        request=request,
        level=constants.INFO,
        message=f"Categoria \"{categoria.categoria}\" alterada para {'' if categoria.essencial else 'não'} essencial"
    )
    return redirect('/perfil/gerenciar/')

