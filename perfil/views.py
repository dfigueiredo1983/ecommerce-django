from django.contrib import messages

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .models import Perfil
from .forms import PerfilForm, UserForm

class BasePerfil(View):
    template_name = 'perfil/criar.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None

        if self.request.user.is_authenticated: # Se autenticado então ele quer atualizar
            self.contexto = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilForm': PerfilForm(
                    data=self.request.POST or None,
                )
            }
        else: # Novo usuário
            self.contexto = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                ),
                'perfilForm': PerfilForm(
                    data=self.request.POST or None,
                )
            }

        self.userForm = self.contexto['userForm']
        self.perfilForm = self.contexto['perfilForm']


        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

class CreatePerfilView(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userForm.is_valid():
            # messages.error(
            #     self.request,
            #     'Existe erros no formulário'
            # )
            return self.renderizar


        return HttpResponse('Criando o perfil')


class UpdatePerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método atualizar pedido do app Perfil')

class LoginPerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método Login pedido do app Perfil')

class LogoutPerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método Logout pedido do app Perfil')

