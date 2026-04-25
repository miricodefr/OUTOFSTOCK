from django.shortcuts import render


# homepage
def home(request):
    return render(request, 'store/home.html')


# product list page
def products(request):
    return render(request, 'store/products.html')


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
