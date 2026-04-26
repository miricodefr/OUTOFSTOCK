from django.shortcuts import render
from .models import Product


# homepage
def home(request):
    return render(request, 'store/home.html')


# collection page, gets products from database
def products(request):
    all_products = Product.objects.all()
    return render(request, 'store/products.html', {'products': all_products})


# single product page
def product_detail(request):
    return render(request, 'store/product_detail.html')


# cart page
def cart(request):
    return render(request, 'store/cart.html')


# dashboard page
def dashboard(request):
    return render(request, 'store/dashboard.html')


# login page
def login_view(request):
    return render(request, 'store/login.html')


# register page
def register(request):
    return render(request, 'store/register.html')
