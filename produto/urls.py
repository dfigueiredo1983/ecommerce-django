from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListProductView.as_view(), name='list'),
    path('<slug>', views.DetailProductView.as_view(), name='detail'),
    path('toAdd/', views.ToAddCartView.as_view(), name='toAdd'),
    path('remove/', views.RemoveFromCartView.as_view(), name='remove'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('finish/', views.FinishView.as_view(), name='finish'),
]