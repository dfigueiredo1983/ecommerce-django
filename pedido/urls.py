from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('payOrder/<int:pk>', views.PayOrderView.as_view(), name='payOrder'),
    path('listOrder/', views.ListOrderView.as_view(), name='listOrder'),
    path('saveOrder/', views.SaveOrderView.as_view(), name='saveOrder'),
    path('detailOrder/', views.DetailOrderView.as_view(), name='detailOrder'),
]