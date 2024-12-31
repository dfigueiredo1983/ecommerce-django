from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)

    data_nascimento = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'})
    )


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação da senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 
                    'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        self.cleaned_data = super().clean()

        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já cadastrado'
        error_msg_email_exists = 'Email já cadastrado'
        error_msg_password_match = 'As senhas devem ser iguais'
        error_msg_password_short = 'Sua senha deve ter pelo menos 6 caracteres'
        error_msg_required_field = 'campo obrigatório'

        # print('User: ', usuario_data)
        # print('User db: ', type(usuario_db))
        # print('User logado: ', self.usuario)

        if self.usuario: # usuário logado - atualização
            # print('LOGADO')
            if usuario_db is None:
                validation_error_msgs['username'] = 'Não pode alterar o nome de usuário'
                raise(forms.ValidationError(validation_error_msgs))


            if self.usuario.username != usuario_db.username:
                validation_error_msgs['username'] = 'Não pode alterar o nome de usuário'

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
                    validation_error_msgs['password2'] = error_msg_password_short

            if not email_data or email_data != self.usuario.email:
                validation_error_msgs['email'] = 'Não pode alterar o email de usuário'
                raise(forms.ValidationError(validation_error_msgs))


        else: # usuário não logado - cadastro
            # print('NÃO LOGADO')
            if usuario_db == None: # usuário ainda não existe no sistema
                if password_data:
                    if password_data != password2_data:
                        validation_error_msgs['password'] = error_msg_password_match
                        validation_error_msgs['password2'] = error_msg_password_match

                    if len(password_data) < 6:
                        validation_error_msgs['password'] = error_msg_password_short
                        validation_error_msgs['password2'] = error_msg_password_short
                else:
                    validation_error_msgs['password'] = error_msg_required_field


                if not email_data:
                    validation_error_msgs['email'] = error_msg_required_field
                    
                if email_db is not None:
                    validation_error_msgs['email'] = error_msg_email_exists

            else:
                validation_error_msgs['username'] = error_msg_user_exists

        if validation_error_msgs:
            # print('Validation: ', validation_error_msgs)
            raise(forms.ValidationError(validation_error_msgs))
