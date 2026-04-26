from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, CartItem, Review, Profile, WishlistItem
import random


DISCOUNT_CODES = {
    'STUDENT10':    10,
    'OUTOFSTOCK15': 15,
    'WELCOME20':    20,
    'GIVEAPLS':     90,
    '10OFF':        10,
}


# homepage — picks 4 random products for the TV screens
def home(request):
    all_ids = list(Product.objects.values_list('id', flat=True))
    picked  = random.sample(all_ids, min(4, len(all_ids)))
    tv      = list(Product.objects.filter(id__in=picked))
    while len(tv) < 4:
        tv.append(None)
    return render(request, 'store/home.html', {'tv_products': tv})


# collection page — gets products from database with search, filter, sort
def products(request):
    all_products = Product.objects.all().select_related('category', 'owner')
    categories   = Category.objects.all()

    query        = request.GET.get('q', '').strip()
    category_id  = request.GET.get('category', '')
    max_price    = request.GET.get('max_price', '')
    brand_filter = request.GET.get('brand', '').strip()
    sort_by      = request.GET.get('sort', 'newest')

    if query:
        all_products = all_products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )
    if category_id:
        all_products = all_products.filter(category__id=category_id)
    if max_price:
        try:
            all_products = all_products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if brand_filter:
        all_products = all_products.filter(brand__icontains=brand_filter)

    sort_map = {
        'newest':     '-id',
        'oldest':     'id',
        'price_asc':  'price',
        'price_desc': '-price',
        'az':         'name',
    }
    all_products = all_products.order_by(sort_map.get(sort_by, '-id'))
    all_brands   = Product.objects.exclude(brand='').values_list('brand', flat=True).distinct()

    sort_options = [
        ('newest',     'Newest'),
        ('oldest',     'Oldest'),
        ('price_asc',  'Price ↑'),
        ('price_desc', 'Price ↓'),
        ('az',         'A–Z'),
    ]
    return render(request, 'store/products.html', {
        'products':       all_products,
        'categories':     categories,
        'all_brands':     all_brands,
        'query':          query,
        'selected_cat':   category_id,
        'selected_price': max_price,
        'selected_brand': brand_filter,
        'sort_by':        sort_by,
        'result_count':   all_products.count(),
        'sort_options':   sort_options,
    })


# single product page — now dynamic
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    recommended = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:3]

    reviews = product.reviews.all()

    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return redirect('product_detail', product_id=product_id)

    return render(request, 'store/product_detail.html', {
        'product':     product,
        'recommended': recommended,
        'reviews':     reviews,
    })


# cart page — shows items from database if logged in
def cart(request):
    cart_items      = []
    subtotal        = 0
    applied_code    = ''
    discount_pct    = 0
    discount_amount = 0
    final_total     = 0

    if request.user.is_authenticated:
        cart_items      = CartItem.objects.filter(user=request.user).select_related('product')
        subtotal        = sum(item.product.price * item.quantity for item in cart_items)
        applied_code    = request.session.get('applied_code', '')
        discount_pct    = request.session.get('discount_pct', 0)
        discount_amount = round(float(subtotal) * discount_pct / 100, 2)
        final_total     = round(float(subtotal) - discount_amount, 2)

    return render(request, 'store/cart.html', {
        'cart_items':      cart_items,
        'total':           subtotal,
        'subtotal':        subtotal,
        'applied_code':    applied_code,
        'discount_pct':    discount_pct,
        'discount_amount': discount_amount,
        'final_total':     final_total,
    })


# add item to cart
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


# remove item from cart
@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')


# simulate checkout — clears the cart
@login_required(login_url='/login/')
def checkout(request):
    CartItem.objects.filter(user=request.user).delete()
    request.session.pop('applied_code', None)
    request.session.pop('discount_pct', None)
    return render(request, 'store/checkout_done.html')


# apply a discount code — stores it in the session
@login_required(login_url='/login/')
def apply_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        if code in DISCOUNT_CODES:
            request.session['applied_code'] = code
            request.session['discount_pct'] = DISCOUNT_CODES[code]
            request.session.pop('code_error', None)
        else:
            request.session['applied_code'] = ''
            request.session['discount_pct'] = 0
            request.session['code_error']   = 'That code is not valid.'
    return redirect('cart')


# remove the discount code from the session
@login_required(login_url='/login/')
def remove_code(request):
    request.session.pop('applied_code', None)
    request.session.pop('discount_pct', None)
    request.session.pop('code_error',   None)
    return redirect('cart')


# dashboard page — requires login, shows user info
@login_required(login_url='/login/')
def dashboard(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'store/dashboard.html', {
        'cart_count': cart_count,
        'cart_items': cart_items,
    })


# login page
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


# register page
def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email    = request.POST.get('email')
        role     = request.POST.get('role', 'buyer')
        if User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'store/register.html', {'error': error})
