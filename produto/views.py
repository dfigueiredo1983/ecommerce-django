from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . models import Produto, Variacao

from django.urls import reverse
from django.http import HttpResponseRedirect

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
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:list'))

        # if self.request.session['carrinho']:
        #     print('Existe o carrinho na sessão')
        #     self.request.session['carrinho'] = {}
        #     # return HttpResponseRedirect(reverse('produto:list'))
        #     return redirect('produto:list')

        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        print(f'Carrinho: {carrinho}')

        if variacao_id in carrinho:
            print('Já existe no carrinho')
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            print(f'Antes. Quantidade no carrinho: {quantidade_carrinho}')
            quantidade_carrinho += 1
            print(f'Depois. Quantidade no carrinho: {quantidade_carrinho}')

            if variacao_estoque < quantidade_carrinho:
                print(f'Estoque insuficiente. Há apenas {variacao_estoque}.')
                messages.warning(
                    self.request,
                    f'Estoque insuficiente. Temos apenas {variacao_estoque} disponíveis',
                )
                return redirect(self.request.META.get('HTTP_REFERER', 'produto:list'))

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                  quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                  quantidade_carrinho
        else:
            print('Ainda não existe no carrinho')
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }
        self.request.session.save()

        print(f'Quantidade no carrinho: {self.request.session['carrinho']}')

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado' \
                ' ao carrinho com sucesso.'
        )

        return redirect(self.request.META.get('HTTP_REFERER', 'produto:list'))
        
        # return HttpResponse('Adicionado ao carrinho de compras')


class CartView(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(
            self.request,
            'produto/carrinho.html',
            context=contexto,
        )

class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:list'))
        variacao_id = self.request.GET.get('vid')

        print(f'Variação para remover do carrinho: {variacao_id}')

        if not variacao_id:
            # messages.error(
            #     self.request,
            #     'Produto não existe no carrinho.'
            # )
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]
        print(f'Carrinho antes de remover: {carrinho}')
        quantidade = carrinho['quantidade']
        if quantidade > 1:
            carrinho['quantidade'] = quantidade - 1
        else:
            del self.request.session['carrinho'][variacao_id]
                
        self.request.session.save()
        print(f'Carrinho depois de remover: {carrinho}')
        
        messages.success(
            self.request,
            f'{carrinho['produto_nome']} removido do carrinho de compras',
        )

        return redirect(http_referer)

class PurchaseSummaryView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            print('Usuário não autenticado')
            return redirect('perfil:create')

        print('Usuário autenticado')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(
            self.request,
            'produto/resumo.html',
            contexto,
        )
