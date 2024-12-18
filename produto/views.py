from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . models import Produto, Variacao

# Create your views here.
class ListProductView(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetailProductView(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class ToAddCartView(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', 'produto:list')

        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {} # se o carrinho não existir
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # TODO: variação existe no carrinho
            pass
        else:
            # TODO: ainda não existe no carrinho
            ...



        print(f'Produto: {variacao.produto} - Nome: {variacao.nome}')

        # messages.error(
        #     self.request,
        #     'Erro ao adicionar ao carrinho'
        # )

        # return redirect(self.request.META.get('HTTP_REFERER', 'produto:list'))
    
        return HttpResponse('Adicionado ao carrinho de compras')


class CartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método carrinho de produtos do app Produto')

class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método remover produto do app Produto')

class FinishView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método finalizar produto do app Produto')
