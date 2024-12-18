from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class CreatePerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método criar pedido do app Perfil')

class UpdatePerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método atualizar pedido do app Perfil')

class LoginPerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método Login pedido do app Perfil')

class LogoutPerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método Logout pedido do app Perfil')

