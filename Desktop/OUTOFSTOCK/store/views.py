from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, CartItem, Review, WishlistItem, Profile, Order, UsedCode, RecentlyViewed, ProductImage
import random

DISCOUNT_CODES = {
    'GIVEAPLS': 0.90,
    '10OFF': 0.10,
}

def get_role(user):
    if user.is_staff:
        return 'admin'
    try:
        return user.profile.role
    except:
        return 'buyer'


def home(request):
    all_products = list(Product.objects.all())
    tv_products = random.sample(all_products, min(4, len(all_products)))
    while len(tv_products) < 4:
        tv_products.append(None)
    return render(request, 'store/home.html', {'tv_products': tv_products})


def products(request):
    items = Product.objects.all()
    top_categories = Category.objects.filter(parent=None)
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    subcategory_id = request.GET.get('subcategory', '')
    max_price = request.GET.get('max_price', '')
    brand_filter = request.GET.get('brand', '')
    sort_by = request.GET.get('sort', 'newest')

    if query:
        items = items.filter(Q(name__icontains=query) | Q(brand__icontains=query))

    if subcategory_id:
        items = items.filter(category__id=subcategory_id)
    elif category_id:
        # get products in this category and also products in subcategories of it
        items = items.filter(Q(category__id=category_id) | Q(category__parent__id=category_id))

    if max_price:
        try:
            items = items.filter(price__lte=float(max_price))
        except:
            pass

    if brand_filter:
        items = items.filter(brand__icontains=brand_filter)

    if sort_by == 'price_asc':
        items = items.order_by('price')
    elif sort_by == 'price_desc':
        items = items.order_by('-price')
    elif sort_by == 'oldest':
        items = items.order_by('id')
    elif sort_by == 'az':
        items = items.order_by('name')
    else:
        items = items.order_by('-id')

    all_brands = Product.objects.exclude(brand='').values_list('brand', flat=True).distinct()

    subcategories = []
    if category_id:
        subcategories = list(Category.objects.filter(parent__id=category_id).values('id', 'name'))

    return render(request, 'store/products.html', {
        'products': items,
        'top_categories': top_categories,
        'categories': categories,
        'subcategories': subcategories,
        'all_brands': all_brands,
        'query': query,
        'selected_cat': category_id,
        'selected_subcat': subcategory_id,
        'selected_price': max_price,
        'selected_brand': brand_filter,
        'sort_by': sort_by,
        'result_count': items.count(),
    })


def subcategories_json(request):
    parent_id = request.GET.get('parent_id', '')
    subs = []
    if parent_id:
        subs = list(Category.objects.filter(parent__id=parent_id).values('id', 'name'))
    return JsonResponse({'subcategories': subs})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('products')

    reviews = product.reviews.all()
    recommended = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    product_images = product.images.all()

    # calculate avg rating manually
    avg_rating = None
    if reviews.count() > 0:
        total = 0
        for r in reviews:
            total += r.rating
        avg_rating = round(total / reviews.count(), 1)

    # save to recently viewed if logged in
    if request.user.is_authenticated:
        RecentlyViewed.objects.filter(user=request.user, product=product).delete()
        RecentlyViewed.objects.create(user=request.user, product=product)
        # only keep 10
        old_views = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')
        ids = list(old_views.values_list('id', flat=True)[:10])
        RecentlyViewed.objects.filter(user=request.user).exclude(id__in=ids).delete()

    # handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = int(request.POST.get('rating', 3))
        comment = request.POST.get('comment', '')

        already = Review.objects.filter(product=product, user=request.user).exists()
        if already:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'error': 'You already reviewed this product.'})
            return redirect('product_detail', product_id=product_id)

        r = Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)

        # recalculate avg
        all_r = product.reviews.all()
        new_total = 0
        for rev in all_r:
            new_total += rev.rating
        new_avg = round(new_total / all_r.count(), 1)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'ok': True,
                'username': request.user.username,
                'rating': r.rating,
                'comment': r.comment,
                'new_avg': new_avg,
                'count': all_r.count(),
            })

        return redirect('product_detail', product_id=product_id)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'product_images': product_images,
        'recommended': recommended,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


def cart(request):
    cart_items = []
    subtotal = 0
    discount_pct = 0
    discount_amt = 0
    total = 0
    applied_code = request.session.get('applied_code', '')

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            subtotal += float(item.product.price) * item.quantity

        if applied_code in DISCOUNT_CODES:
            discount_pct = DISCOUNT_CODES[applied_code]
            discount_amt = round(subtotal * discount_pct, 2)

        total = round(subtotal - discount_amt, 2)
        subtotal = round(subtotal, 2)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_pct': int(discount_pct * 100),
        'discount_amt': discount_amt,
        'total': total,
        'applied_code': applied_code,
    })


@login_required
def apply_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        if code not in DISCOUNT_CODES:
            request.session['code_error'] = 'That code does not exist.'
            request.session['code_success'] = ''
        elif UsedCode.objects.filter(user=request.user, code=code).exists():
            request.session['code_error'] = 'You already used this code.'
            request.session['code_success'] = ''
        else:
            request.session['applied_code'] = code
            request.session['code_error'] = ''
            request.session['code_success'] = code + ' applied! ' + str(int(DISCOUNT_CODES[code] * 100)) + '% off!'
    return redirect('cart')


@login_required
def remove_code(request):
    request.session.pop('applied_code', None)
    request.session.pop('code_error', None)
    request.session.pop('code_success', None)
    return redirect('cart')


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    existing = CartItem.objects.filter(user=request.user, product=product).first()
    if existing:
        existing.quantity += 1
        existing.save()
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=1)
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')


@login_required
def checkout(request):
    applied_code = request.session.get('applied_code', '')
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        price = float(item.product.price) * item.quantity
        if applied_code in DISCOUNT_CODES:
            price = price * (1 - DISCOUNT_CODES[applied_code])

        Order.objects.create(
            buyer=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=round(price, 2),
        )

        # reduce stock
        p = item.product
        p.stock = p.stock - item.quantity
        if p.stock < 0:
            p.stock = 0
        p.save()

    if applied_code:
        UsedCode.objects.get_or_create(user=request.user, code=applied_code)
        request.session.pop('applied_code', None)

    cart_items.delete()
    return render(request, 'store/checkout_done.html')


@login_required
def dashboard(request):
    role = get_role(request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = 0
    for item in cart_items:
        cart_count += item.quantity

    recent_views = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')[:6]

    context = {
        'role': role,
        'cart_items': cart_items,
        'cart_count': cart_count,
        'wishlist_items': WishlistItem.objects.filter(user=request.user),
        'review_count': Review.objects.filter(user=request.user).count(),
        'categories': Category.objects.filter(parent=None),
        'recent_views': recent_views,
    }

    if role == 'seller' or role == 'admin':
        if role == 'admin':
            my_products = Product.objects.all()
            orders = Order.objects.all().order_by('-created_at')
        else:
            my_products = Product.objects.filter(owner=request.user)
            orders = Order.objects.filter(product__owner=request.user).order_by('-created_at')

        total_revenue = 0
        for o in orders:
            total_revenue += float(o.total_price)

        avg_rating_all = None
        all_ratings = Review.objects.filter(product__in=my_products)
        if all_ratings.count() > 0:
            rtotal = 0
            for r in all_ratings:
                rtotal += r.rating
            avg_rating_all = round(rtotal / all_ratings.count(), 1)

        context['my_products'] = my_products
        context['orders'] = orders[:10]
        context['total_revenue'] = round(total_revenue, 2)
        context['total_orders'] = orders.count()
        context['avg_rating_all'] = avg_rating_all
        context['product_count'] = my_products.count()

    if role == 'admin':
        context['total_users'] = User.objects.count()
        context['total_products'] = Product.objects.count()
        context['all_users'] = User.objects.all()
        context['all_categories'] = Category.objects.all()

    return render(request, 'store/dashboard.html', context)


@login_required
def create_listing(request):
    role = get_role(request.user)
    if role != 'seller' and role != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '0')
        stock = request.POST.get('stock', '0')
        brand = request.POST.get('brand', '')
        category_id = request.POST.get('category', '')

        if name and description and category_id:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                owner=request.user,
                category=category,
                name=name,
                description=description,
                brand=brand,
                price=float(price),
                stock=int(stock),
            )

            uploaded_images = request.FILES.getlist('images')
            for i, img_file in enumerate(uploaded_images):
                is_cover = (i == 0)
                prod_img = ProductImage.objects.create(
                    product=product,
                    image=img_file,
                    is_cover=is_cover,
                    order=i,
                )
                if is_cover:
                    product.image = prod_img.image
                    product.save()

    return redirect('dashboard')


@login_required
def edit_listing(request, product_id):
    role = get_role(request.user)
    product = Product.objects.get(id=product_id)

    if role == 'buyer':
        return redirect('dashboard')
    if role == 'seller' and product.owner != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.brand = request.POST.get('brand', product.brand)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)

        cat_id = request.POST.get('category', '')
        if cat_id:
            product.category = Category.objects.get(id=cat_id)

        new_images = request.FILES.getlist('images')
        for i, img_file in enumerate(new_images):
            existing_count = product.images.count()
            is_cover = (existing_count == 0 and i == 0)
            prod_img = ProductImage.objects.create(
                product=product,
                image=img_file,
                is_cover=is_cover,
                order=existing_count + i,
            )
            if is_cover:
                product.image = prod_img.image

        product.save()

    return redirect('dashboard')


@login_required
def delete_listing(request, product_id):
    role = get_role(request.user)
    product = Product.objects.get(id=product_id)

    if role == 'buyer':
        return redirect('dashboard')
    if role == 'seller' and product.owner != request.user:
        return redirect('dashboard')

    product.delete()
    return redirect('dashboard')


@login_required
def create_category(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        parent_id = request.POST.get('parent', '')
        if name:
            parent = None
            if parent_id:
                parent = Category.objects.filter(id=parent_id).first()
            Category.objects.create(name=name, description=description, parent=parent)
    return redirect('dashboard')


@login_required
def edit_category(request, category_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        parent_id = request.POST.get('parent', '')
        if name:
            category.name = name
            category.description = description
            if parent_id and int(parent_id) != category.id:
                category.parent = Category.objects.filter(id=parent_id).first()
            elif not parent_id:
                category.parent = None
            category.save()
    return redirect('dashboard')


@login_required
def delete_category(request, category_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    Category.objects.filter(id=category_id).delete()
    return redirect('dashboard')


@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.user.id != user_id:
        User.objects.filter(id=user_id).delete()
    return redirect('dashboard')


@login_required
def edit_profile(request):
    error = None
    success = None
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if email:
            request.user.email = email
            request.user.save()
        if password:
            if len(password) < 6:
                error = 'Password must be at least 6 characters.'
            else:
                request.user.set_password(password)
                request.user.save()
                login(request, request.user)
        if not error:
            success = 'Profile updated!'
    return render(request, 'store/edit_profile.html', {'error': error, 'success': success})


@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    if not WishlistItem.objects.filter(user=request.user, product=product).exists():
        WishlistItem.objects.create(user=request.user, product=product)
    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product__id=product_id).delete()
    return redirect('dashboard')


@login_required
def delete_product_image(request, image_id):
    role = get_role(request.user)
    prod_image = ProductImage.objects.get(id=image_id)
    product = prod_image.product

    if role == 'buyer':
        return redirect('dashboard')
    if role == 'seller' and product.owner != request.user:
        return redirect('dashboard')

    was_cover = prod_image.is_cover
    prod_image.delete()

    if was_cover:
        next_img = product.images.first()
        if next_img:
            next_img.is_cover = True
            next_img.save()
            product.image = next_img.image
        else:
            product.image = None
        product.save()

    return redirect('dashboard')


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
            error = 'Wrong username or password.'
    return render(request, 'store/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        role = request.POST.get('role', 'buyer')

        if not username or not password or not email:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'store/register.html', {'error': error})
