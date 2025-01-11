from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from produto.models import Variacao
from .models import Pedido, ItemPedido

from utils import utils

# Create your views here.
class PayOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar pedido')

class SaveOrderView(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Favor fazer o login no sistema'
            )
            return redirect('perfil:create')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:list')

        carrinho = self.request.session.get('carrinho')
        print('Carrinho: ', carrinho)
        carrinho_variacoes_ids = [item for item in carrinho]
        print('Keys: ', carrinho_variacoes_ids)
        bd_variacoes = list(
            Variacao.objects.filter(id__in=carrinho_variacoes_ids)
        )

        print(bd_variacoes)

        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtde_carrinho = carrinho[vid]['quantidade']

            preco_unitario = carrinho[vid]['preco_unitario']
            preco_promocional = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtde_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unitario
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                                                    preco_promocional

                error_msg_estoque = 'Estoque insuficiente para alguns itens. ' \
                    'Ajustamos o seu pedido conforme as quantidades ' \
                    'disponíveis em nosso estoque.'
            else:
                carrinho[vid]['preco_quantitativo'] = qtde_carrinho * preco_unitario
                carrinho[vid]['preco_quantitativo_promocional'] = qtde_carrinho * \
                                                    preco_promocional

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque,
                )

                self.request.session.save()
                return redirect('produto:cart')

        qtde_total_carrinho = utils.cart_total_qtde(carrinho)
        valor_total_carrinho = utils.cart_total_valor(carrinho)

        pedido = Pedido(
            user = self.request.user,
            total = valor_total_carrinho,
            qtde_total = qtde_total_carrinho,
            status='C',
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=item['produto_nome'],
                    produto_id=item['produto_id'],
                    variacao=item['variacao_nome'],
                    variacao_id=item['variacao_id'],
                    preco=item['preco_quantitativo'],
                    preco_promocional=item['preco_quantitativo_promocional'],
                    quantidade=item['quantidade'],
                    imagem=item['imagem'],
                )for item in carrinho.values()
            ]
        )

        contexto = {
            'qtde_total_carrinho': qtde_total_carrinho,
            'valor_total_carrinho': valor_total_carrinho,
        }

        renderiza = render(
            self.request,
            self.template_name,
            contexto,
        )

        del self.request.session['carrinho']
        
        return redirect('pedido:listOrder')

        return renderiza

class ListOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método listar pedido do app Pedido')

class DetailOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método detalhar pedido do app Pedido')

