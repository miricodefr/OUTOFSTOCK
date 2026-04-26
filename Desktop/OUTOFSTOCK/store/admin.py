from django.contrib import admin
from .models import Profile, Category, Product, Review, CartItem, WishlistItem, Order, UsedCode


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Order)
admin.site.register(UsedCode)
