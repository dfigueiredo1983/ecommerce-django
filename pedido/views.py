from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class PayOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método pagar pedido do app Pedido')

class SaveOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método fechar pedido do app Pedido')

class DetailOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método detalhar pedido do app Pedido')

