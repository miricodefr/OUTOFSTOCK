from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Review, Profile


# homepage
def home(request):
    return render(request, 'store/home.html')


# collection page, gets products from database
def products(request):
    all_products = Product.objects.all()
    return render(request, 'store/products.html', {'products': all_products})


# single product page — now dynamic
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # simple recommender same category, exclude current product
    recommended = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:3]

    reviews = product.reviews.all()

    # handle review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('product_detail', product_id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommended': recommended,
        'reviews': reviews,
    })


# cart page — shows items from database if logged in
def cart(request):
    cart_items = []
    total = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,            # new
    })


# add item to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1  # already in cart, just increase qty
        cart_item.save()
    return redirect('cart')


# remove item from cart
@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')


# dashboard page — shows user info when logged in
def dashboard(request):
    cart_count = 0
    cart_items = []
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'store/dashboard.html', {
        'cart_count': cart_count, 
        'cart_items': cart_items,  
    })


# login page — handles POST with Django auth
def login_view(request):
    error = None
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password.'
    return render(request, 'store/login.html', {'error': error})


# logout 
def logout_view(request):
    logout(request)
    return redirect('home')


# register page — handles POST to create a new user
def register(request):
    error = None
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role', 'buyer')  
        if User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user, role=role) 
            login(request, user)
            return redirect('dashboard')
    return render(request, 'store/register.html', {'error': error})