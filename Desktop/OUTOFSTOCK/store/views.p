from django.shortcuts import render, get_object_or_404
from .models import Product


# homepage
def home(request):
    return render(request, 'store/home.html')


# products page (collection)
def products(request):
    all_products = Product.objects.all()
    return render(request, 'store/products.html', {'products': all_products})


# single product page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # simple recommender: shows other products from same category
    recommended_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:3]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommended_products': recommended_products
    })


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
    return render(request, 'store/register.html')django.shortcuts import render, get_object_or_404

from .models import Product

# single product page

def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    # simple recommender: shows other products from the same category

    recommended_products = Product.objects.filter(

        category=product.category

    ).exclude(id=product.id)[:3]

    return render(request, 'store/product_detail.html', {

        'product': product,

        'recommended_products': recommended_products

    }
