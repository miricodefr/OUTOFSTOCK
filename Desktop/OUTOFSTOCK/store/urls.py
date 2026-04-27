from django.urls import path
from . import views

urlpatterns = [
    # public pages
    path('',                                    views.home,                 name='home'),
    path('products/',                           views.products,             name='products'),
    path('product/<int:product_id>/',           views.product_detail,       name='product_detail'),

    # AJAX endpoint that returns sub-categories as JSON for a given parent
    path('api/subcategories/',                  views.subcategories_json,   name='subcategories_json'),

    # cart
    path('cart/',                               views.cart,                 name='cart'),
    path('cart/add/<int:product_id>/',          views.add_to_cart,          name='add_to_cart'),
    path('cart/remove/<int:item_id>/',          views.remove_from_cart,     name='remove_from_cart'),
    path('cart/checkout/',                      views.checkout,             name='checkout'),
    path('cart/code/apply/',                    views.apply_code,           name='apply_code'),
    path('cart/code/remove/',                   views.remove_code,          name='remove_code'),

    # dashboard and profile
    path('dashboard/',                          views.dashboard,            name='dashboard'),
    path('profile/edit/',                       views.edit_profile,         name='edit_profile'),

    # listing management
    path('listing/create/',                     views.create_listing,       name='create_listing'),
    path('listing/edit/<int:product_id>/',      views.edit_listing,         name='edit_listing'),
    path('listing/delete/<int:product_id>/',    views.delete_listing,       name='delete_listing'),

    # category management — admins only
    path('category/create/',                    views.create_category,      name='create_category'),
    path('category/edit/<int:category_id>/',    views.edit_category,        name='edit_category'),
    path('category/delete/<int:category_id>/',  views.delete_category,      name='delete_category'),

    # user management — admins only
    path('user/delete/<int:user_id>/',          views.delete_user,          name='delete_user'),

    # wishlist
    path('wishlist/add/<int:product_id>/',      views.add_to_wishlist,      name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',   views.remove_from_wishlist, name='remove_from_wishlist'),

    # image management
    path('image/delete/<int:image_id>/',        views.delete_product_image, name='delete_product_image'),

    # auth
    path('login/',                              views.login_view,           name='login'),
    path('logout/',                             views.logout_view,          name='logout'),
    path('register/',                           views.register,             name='register'),
]
