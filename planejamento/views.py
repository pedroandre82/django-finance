from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from perfil.models import Categoria
from django.views.decorators.csrf import csrf_exempt
import json
from perfil.utils import calcula_total

# Create your views here.

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(
        request=request,
        template_name='definir_planejamento.html', 
        context={'categorias': categorias}
    )


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)

    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    
    total_planejado = calcula_total(categorias, "valor_planejamento")
    total_atingido = sum([categoria.total_gasto() for categoria in categorias])
    porcentagem_atingida = total_atingido * 100 / total_planejado

    return render(
        request=request,
        template_name="ver_planejamento.html",
        context={"categorias": categorias,
                 "total_planejado": f"{total_planejado:,.02f}",
                 "total_atingido": f"{total_atingido:,.02f}",
                 "porcentagem_atingida": int(porcentagem_atingida),
                 }
    )
