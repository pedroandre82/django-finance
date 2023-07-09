from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from extrato.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro, contas_proximas_vencimento, contas_vencidas
from django.db.models import Sum
from datetime import datetime

MESES = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

# Create your views here.
def home(request):
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    # Total de entradas e saidas
    valores = Valores.objects.filter(data__month=mes_atual)
    entradas = valores.filter(tipo="E")
    saidas = valores.filter(tipo="S")
    total_entradas = calcula_total(entradas, "valor")
    total_saidas = calcula_total(saidas, "valor")

    # Contas e total
    contas = Conta.objects.all()
    total_contas = calcula_total(contas, "valor")

    # Equilibrio financeiro
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    # Gastos mensais
    categorias = Categoria.objects.all()
    total_despesas = (
        categorias
        .aggregate(Sum("valor_planejamento"))["valor_planejamento__sum"]
    )
    total_ganhos = sum([categoria.total_recebido() for categoria in categorias])  # mesma coisa?

    # Contas vencidas e proximas ao vencimento
    n_contas_proximas = len(contas_proximas_vencimento())
    n_contas_vencidas = len(contas_vencidas())
    
    return render(request=request, 
                  template_name="home.html",
                  context={'contas': contas,
                           'total_contas': total_contas,
                           'total_entradas': total_entradas,
                           'total_saidas': total_saidas,
                           'percentual_gastos_essenciais': percentual_gastos_essenciais,
                           'percentual_gastos_nao_essenciais': percentual_gastos_nao_essenciais,
                           'total_despesas': f"{total_despesas:,.02f}",
                           'total_ganhos': f"{total_ganhos:,.02f}",
                           'mes_atual': f"{MESES[mes_atual-1]} de {ano_atual}",
                           'contas_proximas': n_contas_proximas,
                           'contas_vencidas': n_contas_vencidas,
                           }
    )


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


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = (
            Valores.objects
            .filter(categoria=categoria)
            .aggregate(Sum('valor'))
            ['valor__sum']
        )

    return render(
        request=request, 
        template_name='dashboard.html', 
        context={'labels': list(dados.keys()), 
                 'values': list(dados.values()),
                }
    )