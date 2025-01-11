from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . models import Produto, Variacao
from perfil.models import Perfil

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

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
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
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'quantidade': quantidade,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'slug': slug,
                'imagem': imagem,
            }
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado' \
                ' ao carrinho com sucesso.'
        )

        return redirect(self.request.META.get('HTTP_REFERER', 'produto:list'))
        

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

        # del self.request.session['carrinho']

        if not variacao_id:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        quantidade = carrinho['quantidade']
        print('Quantidade: ', quantidade)


        print('Carrinho antes de remover: ', carrinho)

        quantidade -= 1
        carrinho['quantidade'] = quantidade
        carrinho['preco_quantitativo'] = quantidade * \
                        carrinho['preco_unitario']

        carrinho['preco_quantitativo_promocional'] = quantidade * \
                        carrinho['preco_unitario_promocional']

        if quantidade == 0:
            messages.success(
                self.request,
                f'{carrinho['produto_nome']} removido do carrinho.',
            )
            del self.request.session['carrinho'][variacao_id]
        else:
            messages.success(
                self.request,
                f'{carrinho['produto_nome']} com {quantidade} unidades no carrinho.',
            )

        
        self.request.session.save()

        return redirect(http_referer)

class PurchaseSummaryView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:create')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuário cadastrado mas ainda não tem perfil no sistema. '
                'Favor preencher os dados do formulário.'
            )
            return redirect('perfil:create')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Usuário não tem itens no carrinho de compras.'
            )
            return redirect('produto:list')

        carrinho = self.request.session['carrinho']
        print('Carrinho Puschase: ', carrinho)

        contexto = {
            'usuario': self.request.user,
            'carrinho': carrinho,
        }

        return render(
            self.request,
            'produto/resumo.html',
            contexto,
        )
