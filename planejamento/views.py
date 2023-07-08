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

#TODO: validar o novo_valor

    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()

    # TODO: Barra de total

    return render(
        request=request,
        template_name="ver_planejamento.html",
        context={"categorias": categorias}
    )
