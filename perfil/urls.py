from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.CreatePerfilView.as_view(), name='create'),
    path('update/', views.UpdatePerfilView.as_view(), name='update'),
    path('login/', views.LoginPerfilView.as_view(), name='login'),
    path('logout/', views.LogoutPerfilView.as_view(), name='logout'),
]