from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Sum
from .models import Product, Category, CartItem, Review, WishlistItem, Profile, Order, UsedCode
import random


# discount codes and the percent they take off
# 0.10 means 10 percent off and 0.90 means 90 percent off
DISCOUNT_CODES = {
    'GIVEAPLS': 0.90,
    '10OFF':    0.10,
}


# helper that returns the role of any logged in user
def get_role(user):
    if user.is_staff:
        return 'admin'
    try:
        return user.profile.role
    except Exception:
        return 'buyer'


# home page view
# picks 4 random products to show on the TV screens
def home(request):
    all_ids = list(Product.objects.values_list('id', flat=True))
    picked_ids = random.sample(all_ids, min(4, len(all_ids)))
    tv_products = list(Product.objects.filter(id__in=picked_ids))

    # pad the list with None if there are fewer than 4 products
    while len(tv_products) < 4:
        tv_products.append(None)

    return render(request, 'store/home.html', {'tv_products': tv_products})


# collection page view
# shows all products and handles search and filter from the URL parameters
def products(request):
    all_products = Product.objects.all().select_related('category', 'owner')
    categories   = Category.objects.all()

    # read whatever the user typed or selected in the filter form
    query        = request.GET.get('q', '').strip()
    category_id  = request.GET.get('category', '')
    max_price    = request.GET.get('max_price', '')
    brand_filter = request.GET.get('brand', '').strip()
    sort_by      = request.GET.get('sort', 'newest')

    # search by product name or brand name
    if query:
        all_products = all_products.filter(
            Q(name__icontains=query) | Q(brand__icontains=query)
        )

    # filter by category if one was selected
    if category_id:
        all_products = all_products.filter(category__id=category_id)

    # filter by max price if one was selected
    if max_price:
        try:
            all_products = all_products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # filter by brand if one was selected
    if brand_filter:
        all_products = all_products.filter(brand__icontains=brand_filter)

    # sort the results based on what the user picked
    sort_map = {
        'newest':     '-id',
        'oldest':     'id',
        'price_asc':  'price',
        'price_desc': '-price',
        'az':         'name',
    }
    all_products = all_products.order_by(sort_map.get(sort_by, '-id'))
    all_brands   = Product.objects.exclude(brand='').values_list('brand', flat=True).distinct()

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
    })


# single product page view
# also handles the review form submission via POST
def product_detail(request, product_id):
    product     = get_object_or_404(Product, id=product_id)
    recommended = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    reviews     = product.reviews.all().select_related('user')
    avg_rating  = reviews.aggregate(avg=Avg('rating'))['avg']

    # if a logged in user submitted the review form save it and reload the page
    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('product_detail', product_id=product_id)

    return render(request, 'store/product_detail.html', {
        'product':     product,
        'recommended': recommended,
        'reviews':     reviews,
        'avg_rating':  avg_rating,
    })


# cart page view
# reads the users cart items and applies any active discount code
def cart(request):
    cart_items   = []
    subtotal     = 0
    discount_pct = 0
    discount_amt = 0
    total        = 0
    applied_code = request.session.get('applied_code', '')

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        subtotal   = sum(item.product.price * item.quantity for item in cart_items)

        # apply discount if there is an active code in the session
        if applied_code and applied_code in DISCOUNT_CODES:
            discount_pct = DISCOUNT_CODES[applied_code]
            discount_amt = round(subtotal * discount_pct, 2)

        total = round(float(subtotal) - float(discount_amt), 2)

    return render(request, 'store/cart.html', {
        'cart_items':   cart_items,
        'subtotal':     subtotal,
        'discount_pct': int(discount_pct * 100),
        'discount_amt': discount_amt,
        'total':        total,
        'applied_code': applied_code,
    })


# apply discount code view
# checks the code is valid and not already used by this user
@login_required
def apply_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()

        if code not in DISCOUNT_CODES:
            request.session['code_error']   = 'That code does not exist.'
            request.session['code_success'] = ''
        elif UsedCode.objects.filter(user=request.user, code=code).exists():
            request.session['code_error']   = 'You have already used that code.'
            request.session['code_success'] = ''
        else:
            request.session['applied_code'] = code
            request.session['code_error']   = ''
            request.session['code_success'] = code + ' applied. ' + str(int(DISCOUNT_CODES[code] * 100)) + ' percent off!'

    return redirect('cart')


# remove discount code view
# clears the active code from the session
@login_required
def remove_code(request):
    request.session.pop('applied_code', None)
    request.session.pop('code_error',   None)
    request.session.pop('code_success', None)
    return redirect('cart')


# add to cart view
# creates or increments a cart item for the logged in user
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    # if the item was already in the cart just increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


# remove from cart view
# deletes a single cart row belonging to the logged in user
@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')


# checkout view
# turns each cart item into an Order row then clears the cart
@login_required
def checkout(request):
    applied_code = request.session.get('applied_code', '')
    cart_items   = CartItem.objects.filter(user=request.user).select_related('product')

    for item in cart_items:
        line_total = float(item.product.price) * item.quantity
        # apply the discount to each line if a code is active
        if applied_code and applied_code in DISCOUNT_CODES:
            line_total = line_total * (1 - DISCOUNT_CODES[applied_code])
        Order.objects.create(
            buyer=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=round(line_total, 2),
        )

    # mark the code as used so the same user cannot use it again
    if applied_code:
        UsedCode.objects.get_or_create(user=request.user, code=applied_code)
        request.session.pop('applied_code', None)

    cart_items.delete()
    return render(request, 'store/checkout_done.html')


# dashboard view
# builds a different context depending on whether the user is a buyer, seller or admin
@login_required
def dashboard(request):
    role       = get_role(request.user)
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_count = sum(item.quantity for item in cart_items)

    ctx = {
        'role':           role,
        'cart_items':     cart_items,
        'cart_count':     cart_count,
        'wishlist_items': WishlistItem.objects.filter(user=request.user).select_related('product'),
        'review_count':   Review.objects.filter(user=request.user).count(),
        'categories':     Category.objects.all(),
    }

    # extra data for sellers and admins
    if role in ('seller', 'admin'):
        if role == 'admin':
            # admins see everything
            my_products = Product.objects.all().select_related('category', 'owner')
            orders      = Order.objects.select_related('product', 'buyer').order_by('-created_at')
        else:
            # sellers only see their own products and orders
            my_products = Product.objects.filter(owner=request.user).select_related('category')
            orders      = Order.objects.filter(
                product__owner=request.user
            ).select_related('product', 'buyer').order_by('-created_at')

        total_revenue  = orders.aggregate(t=Sum('total_price'))['t'] or 0
        avg_rating_all = Review.objects.filter(product__in=my_products).aggregate(avg=Avg('rating'))['avg']

        ctx.update({
            'my_products':    my_products,
            'orders':         orders[:10],
            'total_revenue':  total_revenue,
            'total_orders':   orders.count(),
            'avg_rating_all': avg_rating_all,
            'product_count':  my_products.count(),
        })

    # extra data only for admins
    if role == 'admin':
        ctx.update({
            'total_users':    User.objects.count(),
            'total_products': Product.objects.count(),
            'all_users':      User.objects.select_related('profile').all(),
        })

    return render(request, 'store/dashboard.html', ctx)


# create listing view
# only sellers and admins can access this
@login_required
def create_listing(request):
    role = get_role(request.user)
    if role not in ('seller', 'admin'):
        return redirect('dashboard')

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price', '0')
        stock       = request.POST.get('stock', '0')
        brand       = request.POST.get('brand', '').strip()
        category_id = request.POST.get('category', '')
        image       = request.FILES.get('image')

        if name and description and category_id:
            category = get_object_or_404(Category, id=category_id)
            product  = Product.objects.create(
                owner=request.user,
                category=category,
                name=name,
                description=description,
                brand=brand,
                price=float(price) if price else 0,
                stock=int(stock)   if stock else 0,
            )
            if image:
                product.image = image
                product.save()

    return redirect('dashboard')


# edit listing view
# sellers can only edit their own products but admins can edit any product
@login_required
def edit_listing(request, product_id):
    role    = get_role(request.user)
    product = get_object_or_404(Product, id=product_id)

    if role == 'buyer':
        return redirect('dashboard')
    if role == 'seller' and product.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        product.name        = request.POST.get('name', product.name).strip()
        product.description = request.POST.get('description', product.description).strip()
        product.brand       = request.POST.get('brand', product.brand).strip()
        product.price       = request.POST.get('price', product.price)
        product.stock       = request.POST.get('stock', product.stock)
        cat_id = request.POST.get('category', '')
        if cat_id:
            product.category = get_object_or_404(Category, id=cat_id)
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()

    return redirect('dashboard')


# delete listing view
# sellers can only delete their own products but admins can delete any product
@login_required
def delete_listing(request, product_id):
    role    = get_role(request.user)
    product = get_object_or_404(Product, id=product_id)

    if role == 'buyer':
        return redirect('dashboard')
    if role == 'seller' and product.owner != request.user:
        return redirect('dashboard')

    product.delete()
    return redirect('dashboard')


# create category view
# only admins can create categories
@login_required
def create_category(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        if name:
            Category.objects.create(name=name, description=description)

    return redirect('dashboard')


# delete category view
# only admins can delete categories
@login_required
def delete_category(request, category_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    Category.objects.filter(id=category_id).delete()
    return redirect('dashboard')


# delete user view
# only admins can delete users and they cannot delete themselves
@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.user.id != user_id:
        User.objects.filter(id=user_id).delete()
    return redirect('dashboard')


# edit profile view
# lets any logged in user update their email or password
@login_required
def edit_profile(request):
    error   = None
    success = None

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if email:
            request.user.email = email
            request.user.save()

        if password:
            if len(password) < 6:
                error = 'Password must be at least 6 characters.'
            else:
                request.user.set_password(password)
                request.user.save()
                # log the user back in after a password change
                login(request, request.user)

        if not error:
            success = 'Profile updated successfully.'

    return render(request, 'store/edit_profile.html', {'error': error, 'success': success})


# add to wishlist view
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', product_id=product_id)


# remove from wishlist view
@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product__id=product_id).delete()
    return redirect('dashboard')


# login view
# authenticates the user and redirects them to the dashboard
def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Wrong username or password. Please try again.'

    return render(request, 'store/login.html', {'error': error})


# logout view
def logout_view(request):
    logout(request)
    return redirect('home')


# register view
# creates a new User and Profile then logs the user in right away
def register(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email    = request.POST.get('email', '').strip()
        role     = request.POST.get('role', 'buyer')

        if not username or not password or not email:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.objects.filter(username=username).exists():
            error = 'That username is already taken.'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'store/register.html', {'error': error})
