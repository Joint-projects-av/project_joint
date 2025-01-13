from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Product, Category, Cart, CartItem, Order, OrderItem


# Create your views here.


class IndexView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class AddToCartView(View):
    def post(self, request, product_id):
        # Получаем корзину пользователя (если ее нет — создаем новую)
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Получаем товар по ID
        product = Product.objects.get(id=product_id)

        # Проверяем, есть ли уже этот товар в корзине
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            # Если товар был добавлен впервые, установим количество в 1
            cart_item.quantity = 1
            cart_item.save()
            messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
        else:
            # Если товар уже в корзине, увеличиваем его количество на 1
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Количество товара "{product.name}" увеличено на 1.')

        return redirect('cart')


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


class ProductsByCategoryView(View):
    template_name = 'shop/products_by_category.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, self.template_name, {
            'category': category,
            'products': products,
        })



class RegisterView(View):
    template_name = 'shop/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'shop/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class CartView(LoginRequiredMixin, View):
    template_name = 'shop/cart.html'

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        total_cost = cart.get_total_cost()
        return render(request, self.template_name, {
            'cart': cart,
            'items': items,
            'total_cost': total_cost
        })



class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.cartitem_set.exists():
            messages.error(request, "Корзина пуста.")
            return redirect('cart')

        # Создаем заказ
        order = Order.objects.create(user=request.user)

        # Копируем товары из корзины в заказ и сохраняем цену каждого товара
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Очищаем корзину
        cart.cartitem_set.all().delete()

        messages.success(request, f"Ваш заказ №{order.id} успешно оформлен!")
        return redirect('order_history')



class OrderHistoryView(LoginRequiredMixin, View):
    template_name = 'shop/order_history.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, self.template_name, {'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'shop/order_detail.html'

    def get(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if not order:
            messages.error(request, "Заказ не найден.")
            return redirect('order_history')

        return render(request, self.template_name, {'order': order})
