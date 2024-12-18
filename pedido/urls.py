from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('payOrder/', views.PayOrderView.as_view(), name='payOrder'),
    path('closeOrder/', views.CloseOrderView.as_view(), name='closeOrder'),
    path('detailOrder/', views.DetailOrderView.as_view(), name='detailOrder'),
]