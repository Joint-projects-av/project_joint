from django.urls import path
from .views import (
    IndexView, ProductDetailView, CategoryListView, RegisterView, LoginView, LogoutView,
    CartView, AddToCartView, OrderHistoryView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
]