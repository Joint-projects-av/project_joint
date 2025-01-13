from django.urls import path
from .views import (
    IndexView, ProductDetailView, CategoryListView, RegisterView, LoginView, LogoutView,
    CartView, AddToCartView, OrderHistoryView, ProductsByCategoryView, CheckoutView, OrderDetailView,
    ProductSearchByBrandView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('brands/<int:brand_id>/', ProductSearchByBrandView.as_view(), name='products_by_brand'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]