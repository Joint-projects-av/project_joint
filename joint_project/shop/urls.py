from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category, name='category'),
    path('detail_goods/<int:pk>/', views.detail_goods, name='detail_goods'),
    path('login/', views.login_view, name='login'),
    path('order-history/', views.order_history, name='order_history'),
]
