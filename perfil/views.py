from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse

from .models import Perfil
from .forms import PerfilForm, UserForm

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import copy


class BasePerfil(View):
    template_name = 'perfil/criar.html'
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.perfil = None

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        if self.request.user.is_authenticated: # Se autenticado então ele quer atualizar
            self.perfil = Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userForm': UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilForm': PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
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

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'


        self.renderizar = render(self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

class CreatePerfilView(BasePerfil):
    def post(self, *args, **kwargs):

        if not self.userForm.is_valid() or not self.perfilForm.is_valid():
            return self.renderizar

        username = self.userForm.cleaned_data.get('username')
        password = self.userForm.cleaned_data.get('password')
        email = self.userForm.cleaned_data.get('email')
        first_name = self.userForm.cleaned_data.get('first_name')
        last_name = self.userForm.cleaned_data.get('last_name')

        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfilForm.cleaned_data['usuario'] = usuario
                perfil = Perfil(**self.perfilForm.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilForm.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # usuário não logado, criar o usuário
        else:
            usuario = self.userForm.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilForm.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
                )
            if autentica:
                login(self.request, user=usuario)

        # Caso seja criada uma nova seção por causa da troca de senha do usuário
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Usuário cadastrado com sucesso.'
        )

        return redirect('perfil:create')

class UpdatePerfilView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Método atualizar pedido do app Perfil')

class LoginPerfilView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        print(f'Usuário: {username} - Password: {password}')

        if username == '' or password == '':
            messages.error(
                self.request,
                'Favor inserir usuário ou senha.'
            )
            return redirect('perfil:create')

        usuario = authenticate(
            self.request,
            username=username,
            password=password,
        )

        print('autentica: ', usuario)

        if not usuario:
            messages.error(
                self.request,
                'Usuário ou senha inválidos.'
            )
            return redirect('perfil:create')
        
        login(self.request, user=usuario)
        messages.success(
            self.request,
            'Login realizado com sucesso.'
        )
        return redirect('produto:list')


class LogoutPerfilView(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:list')

