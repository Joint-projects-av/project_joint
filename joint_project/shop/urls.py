from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category, name='category'),
    path('goods/<int:pk>/', views.detain_goods, name='detain_goods'),
]
